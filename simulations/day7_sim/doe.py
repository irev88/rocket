"""
doe.py — Day 7 Arc B2/B3: design-of-experiments sensitivity (Latin hypercube,
Spearman ranking) and trajectory optimization (differential evolution) for the
two leading repair configurations:

  Config A "L1": 600 t GLOM, 1x MVac, margin->prop (S2 prop 119 t), 20 t payload
  Config B "L2": 600.55 t, 2x MVac (+0.55 t dry), margin->prop, 20 t payload

Outputs: results/S8_sensitivity.json (B2), results/S9_optimized.json (B3),
         results/S8_samples_{A,B}.json (raw LHS samples for figures)
"""
import json, math, os, time
import numpy as np
from scipy.stats import qmc, spearmanr
from scipy.optimize import differential_evolution
import params as P
import vehicle as V
import sim

OUT = os.path.join(os.path.dirname(__file__), "results")

CONFIGS = dict(
    A=dict(base=dict(m_s1_prop=391e3, m_s2_prop=119e3, m_margin=0.0,
                     m_payload=20e3, n_eng_s2=1, jettison_fairing=True,
                     label="A_1xMVac_m2p"),
           grid_deficit=1467.0),
    B=dict(base=dict(m_s1_prop=391e3, m_s2_prop=119e3, m_margin=0.0,
                     m_payload=20e3, n_eng_s2=2, m_s2_dry=P.M_S2_DRY + 550.0,
                     jettison_fairing=True, label="B_2xMVac_m2p"),
           grid_deficit=872.0),
)

# factor bounds (B2 LHS & B3 DE share the guidance subset)
BOUNDS = dict(kick=(2.5, 6.0), t_kick0=(10.0, 20.0), bias0=(0.0, 28.0),
              hold=(160.0, 360.0), p1=(350.0, 391.0), cd=(0.8, 1.2))
FACTORS = ["kick", "t_kick0", "bias0", "hold", "p1", "cd"]


def build_cfg(name, x):
    """x dict with factor values -> sim.Config"""
    b = dict(CONFIGS[name]["base"])
    b.update(pitch_kick=math.radians(x["kick"]),
             t_kick0=x["t_kick0"], t_kick1=x["t_kick0"] + 18.0,
             s2_guidance="schedule",
             s2_bias0=math.radians(x["bias0"]), s2_bias_hold=x["hold"],
             m_s1_prop=x.get("p1", 391.0) * 1000.0)
    return sim.Config(**b)


def evaluate(name, x, want_series=False):
    """returns dict of responses; converged=False marks crashes/no-orbit."""
    V.set_dispersion(cd=x.get("cd", 1.0))
    try:
        res = sim.run(build_cfg(name, x), record_dt=5.0)
    finally:
        V.clear_dispersion()
    conv = ("SECO" in res["events"]) and res["orbit"] is not None \
        and not math.isnan(res.get("deficit_to_500x500", float("nan")))
    out = dict(converged=bool(conv))
    if conv:
        meco = res["events"]["MECO"]
        out.update(deficit=res["deficit_to_500x500"],
                   q_max_kpa=res["q_max"] / 1000.0,
                   meco_v=meco["v"], meco_h_km=meco["h"] / 1000.0,
                   meco_gamma_deg=meco["gamma"],  # events store degrees already
                   dv_drag=res["losses"]["I_drag"],
                   dv_steer=res["losses"]["I_steer"],
                   dv_grav_s2=res["losses"]["I_grav_s2"],
                   t_seco=res["events"]["SECO"]["t"],
                   g_max=res["g_max"])
    return out


# ---------------------------------------------------------------- B2: LHS DOE
def run_lhs(name, n=600, seed=42):
    rng = qmc.LatinHypercube(d=len(FACTORS), seed=seed)
    u = rng.random(n)
    lo = np.array([BOUNDS[f][0] for f in FACTORS])
    hi = np.array([BOUNDS[f][1] for f in FACTORS])
    X = lo + u * (hi - lo)
    rows = []
    t0 = time.time()
    for i, xi in enumerate(X):
        x = dict(zip(FACTORS, xi))
        r = evaluate(name, x)
        rows.append(dict(**{f: round(x[f], 4) for f in FACTORS}, **r))
    json.dump(rows, open(os.path.join(OUT, f"S8_samples_{name}.json"), "w"))
    conv = [r for r in rows if r["converged"]]
    fail = len(rows) - len(conv)
    # failure fraction per factor tertile (which corners kill?)
    failmap = {}
    for f in FACTORS:
        vals = np.array([r[f] for r in rows])
        edges = np.quantile(vals, [0, 1 / 3, 2 / 3, 1.0])
        fr = []
        for k in range(3):
            sel = [r for r in rows if edges[k] <= r[f] <= edges[k + 1] + 1e-9]
            fr.append(round(100 * (1 - sum(r["converged"] for r in sel) / max(len(sel), 1)), 1))
        failmap[f] = fr
    # Spearman on converged subset
    spear = {}
    for metric in ("deficit", "q_max_kpa", "meco_v", "meco_h_km", "dv_steer", "dv_drag"):
        ys = np.array([r[metric] for r in conv])
        per = {}
        for f in FACTORS:
            xs = np.array([r[f] for r in conv])
            rho, p = spearmanr(xs, ys)
            per[f] = dict(rho=round(float(rho), 3), p=round(float(p), 4))
        spear[metric] = per
    ranked = sorted(FACTORS, key=lambda f: -abs(spear["deficit"][f]["rho"]))
    summary = dict(config=name, n=n, n_converged=len(conv), n_failed=fail,
                   fail_pct=round(100 * fail / n, 1),
                   fail_pct_by_factor_tertile=failmap,
                   spearman=spear,
                   deficit_drivers_ranked=ranked,
                   deficit_stats=dict(mean=round(float(np.mean([r["deficit"] for r in conv])), 0),
                                      p5=round(float(np.percentile([r["deficit"] for r in conv], 5)), 0),
                                      p95=round(float(np.percentile([r["deficit"] for r in conv], 95)), 0)),
                   runtime_s=round(time.time() - t0, 1))
    return summary


# ---------------------------------------------------------------- B3: DE optimization
def run_de(name, maxiter=40, popsize=8, seed=7):
    gv = ["kick", "t_kick0", "bias0", "hold"]
    bounds = [BOUNDS[f] for f in gv]
    hist = []
    evals = [0]

    def obj(u):
        x = dict(zip(gv, u)); x.update(p1=391.0, cd=1.0)
        r = evaluate(name, x)
        evals[0] += 1
        if not r["converged"]:
            c = 10000.0
        else:
            c = r["deficit"]
            if r["q_max_kpa"] > P.Q_STRUCT / 1000.0:
                c += 25.0 * (r["q_max_kpa"] - P.Q_STRUCT / 1000.0)
            if r["meco_h_km"] < 50.0:
                c += 30.0 * (50.0 - r["meco_h_km"])
            if r["g_max"] and r["g_max"] > P.G_AXIAL_MAX:
                c += 50.0 * (r["g_max"] - P.G_AXIAL_MAX)
        if not hist or c < hist[-1][1]:
            hist.append((evals[0], c))
        return c

    t0 = time.time()
    res = differential_evolution(obj, bounds, maxiter=maxiter, popsize=popsize,
                                 tol=0.002, seed=seed, polish=True,
                                 updating="immediate", workers=1)
    x = dict(zip(gv, [float(v) for v in res.x])); x.update(p1=391.0, cd=1.0)
    r = evaluate(name, x)
    out = dict(config=name, success=bool(res.success),
               x_opt={k: round(v, 4) for k, v in x.items()},
               fun=round(float(res.fun), 1), responses=r,
               grid_tuned_deficit=CONFIGS[name]["grid_deficit"],
               improvement_vs_grid=round(CONFIGS[name]["grid_deficit"] - float(res.fun), 0),
               n_evals=evals[0], runtime_s=round(time.time() - t0, 1),
               history=[(e, round(c, 0)) for e, c in hist])
    return out


if __name__ == "__main__":
    s8 = {}
    for nm in ("A", "B"):
        print(f"B2 — LHS DOE config {nm} (600 samples) ...", flush=True)
        s8[nm] = run_lhs(nm)
        print(f"  converged {s8[nm]['n_converged']}/600; deficit drivers: "
              f"{s8[nm]['deficit_drivers_ranked']}")
        for f in s8[nm]["deficit_drivers_ranked"][:4]:
            print(f"    deficit~{f}: rho={s8[nm]['spearman']['deficit'][f]['rho']:+.3f}")
    json.dump(s8, open(os.path.join(OUT, "S8_sensitivity.json"), "w"), indent=1)

    s9 = {}
    for nm in ("A", "B"):
        print(f"B3 — differential evolution config {nm} ...", flush=True)
        s9[nm] = run_de(nm)
        o = s9[nm]
        print(f"  x*={o['x_opt']}  -> deficit {o['fun']} m/s "
              f"(grid {o['grid_tuned_deficit']:.0f}, gain {o['improvement_vs_grid']:.0f})"
              f"  q={o['responses'].get('q_max_kpa')} kPa")
    json.dump(s9, open(os.path.join(OUT, "S9_optimized.json"), "w"), indent=1)
