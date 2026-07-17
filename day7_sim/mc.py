"""
mc.py — Day 7 Arc B5: Monte-Carlo robustness.

Part 1 (ascent): 400 samples per leading config (A: 1xMVac+m2p @ DE-optimum,
B: 2xMVac+m2p @ DE-optimum).  Dispersions (Normal, 2-sigma shown):
  S1/S2 Isp  +/-1.5 s,  Cd +/-10%,  stage dry masses +/-1%,
  kick execution +/-0.15 deg,  t_kick0 +/-1.0 s.

Part 2 (recovery): 500 samples per plan
  P0 "documented": 58 t stack, 18 t reserve, deepest reachable entry (tl 0.67)
  P1 "sized M2.3": 72.4 t stack, 32.4 t reserve, corridor Mach 2.3 (tl 0.85)
Dispersions: CD_A ~ U(12,32) m^2,  L/D ~ U(1.04,1.56),  entry throttle
execution ~ N(1,2.5%),  S1 Isp +/-1.0 s (2-sigma).  Landing ignition is
re-targeted per sample (adaptive guidance assumption).

Outputs: results/S10_mc_ascent.json, results/S11_mc_recovery.json
"""
import json, math, os, time
import numpy as np
import params as P
import atmosphere as AT
import vehicle as V
import sim
import recovery_sim as RS
from doe import CONFIGS, evaluate, build_cfg
import run_recovery as RR

OUT = os.path.join(os.path.dirname(__file__), "results")
S9 = json.load(open(os.path.join(OUT, "S9_optimized.json")))
rng = np.random.default_rng(20260717)


def stats(a, p=(5, 50, 95)):
    a = np.asarray(a, float)
    return dict(mean=round(float(a.mean()), 2), sd=round(float(a.std()), 2),
                **{f"p{q}": round(float(np.percentile(a, q)), 2) for q in p})


# ------------------------------------------------------------- Part 1: ascent
def mc_ascent(name, n=400):
    x0 = {k: v for k, v in S9[name]["x_opt"].items()}
    rows = []
    for _ in range(n):
        x = dict(x0)
        x["kick"] = max(0.5, x["kick"] + rng.normal(0, 0.075))
        x["t_kick0"] = max(6.0, x["t_kick0"] + rng.normal(0, 0.5))
        cd = float(np.clip(rng.normal(1.0, 0.05), 0.85, 1.15))
        i1, i2 = rng.normal(0, 0.75), rng.normal(0, 0.75)
        s1d = float(np.clip(rng.normal(1.0, 0.005), 0.985, 1.015))
        s2d = float(np.clip(rng.normal(1.0, 0.005), 0.985, 1.015))
        V.set_dispersion(isp1=i1, isp2=i2, cd=cd)
        try:
            b = dict(CONFIGS[name]["base"])
            b.update(pitch_kick=math.radians(x["kick"]), t_kick0=x["t_kick0"],
                     t_kick1=x["t_kick0"] + 18.0, s2_guidance="schedule",
                     s2_bias0=math.radians(x["bias0"]), s2_bias_hold=x["hold"],
                     m_s1_prop=x["p1"] * 1000.0,
                     m_s2_dry=CONFIGS[name]["base"].get("m_s2_dry", P.M_S2_DRY) * s2d)
            # scale S1 dry constituents
            m_s1_dry = (P.M_S1_STRUCT + P.M_S1_ENG + P.M_REC_HW) * s1d
            b.update(m_s1_dry=m_s1_dry)
            res = sim.run(sim.Config(**b), record_dt=5.0)
        finally:
            V.clear_dispersion()
        conv = ("SECO" in res["events"]) and res["orbit"] is not None
        r = dict(converged=bool(conv))
        if conv:
            r.update(deficit=res["deficit_to_500x500"], q_kpa=res["q_max"] / 1000.0,
                     g=res["g_max"], meco_v=res["events"]["MECO"]["v"],
                     perigee_km=res["orbit"]["perigee_km"])
        rows.append(r)
    cv = [r for r in rows if r["converged"]]
    out = dict(config=name, n=n, n_converged=len(cv), fail_pct=round(100 * (1 - len(cv) / n), 1),
               nominal_deficit=S9[name]["responses"]["deficit"],
               deficit=stats([r["deficit"] for r in cv]),
               q_max_kpa=stats([r["q_kpa"] for r in cv], p=(50, 95, 99)),
               g_max=stats([r["g"] for r in cv], p=(50, 95, 99)),
               meco_v=stats([r["meco_v"] for r in cv]),
               P_q_gt_35kpa=round(float(np.mean([r["q_kpa"] > 35.0 for r in cv])), 3),
               P_g_gt_5=round(float(np.mean([r["g"] > 5.0 for r in cv])), 3),
               P_deficit_le_0=round(float(np.mean([r["deficit"] <= 0 for r in cv])), 3),
               dispersion_assumptions="Normal 2-sigma: Isp +/-1.5 s, Cd +/-10%, dry +/-1%, "
                                      "kick +/-0.15 deg, t_kick0 +/-1 s")
    json.dump(rows, open(os.path.join(OUT, f"S10_samples_{name}.json"), "w"))
    return out


# ----------------------------------------------------------- Part 2: recovery
def mc_recovery(plan, n=500):
    if plan == "P0_documented":
        m_sep, tl_plan, reserve_t, corridor = 58_000.0, 0.67, 18.0, None
    else:
        m_sep, tl_plan, reserve_t, corridor = 72_400.0, 0.85, 32.4, 2.3
    rows = []
    vx0, vh0, x0, h0_ = RR.VX0, RR.VH0, RR.SEP["x"], RR.SEP["h"]
    for _ in range(n):
        cda = float(rng.uniform(12.0, 32.0))
        ld = float(rng.uniform(1.04, 1.56))
        tl = float(np.clip(tl_plan * (1 + rng.normal(0, 0.025)), 0.40, 1.00))
        V.set_dispersion(isp1=rng.normal(0, 0.5))
        RS.CD_A_STAGE = cda
        try:
            rows_tr, log, st = RS.integrate(
                (0.0, x0, h0_, vx0, vh0, m_sep),
                [dict(kind="ballistic", exit_h=70_000.0),
                 dict(kind="entry_burn", n_eng=3, throttle=tl, exit_h=40_000.0,
                      m_floor=RR.M_FLOOR),
                 dict(kind="glide", LD=ld, exit_h=RR.GLIDE_EXIT_H)], record=False)
            eb, ge = log["entry_burn_exit"], log["glide_exit"]
        finally:
            V.clear_dispersion()
            RS.CD_A_STAGE = 18.0
        if eb["m"] <= RR.M_FLOOR + 50.0 or ge["h"] <= -40.0:
            rows.append(dict(ok=False, why="entry reserve exhausted/impact"))
            continue
        entry_t = (m_sep - eb["m"]) / 1000.0
        mach = eb["v"] / AT.sound_speed(eb["h"])
        # adaptive landing re-target
        win = RS.solve_hover_slam_ignition(abs(ge["vh"]), ge["h"], eb["m"], 0.0)
        sel = RR.feasible_sol(win)
        if sel is None:
            rows.append(dict(ok=False, why="landing infeasible", mach=mach,
                             entry_t=entry_t, x_km=ge["x"] / 1000.0))
            continue
        land_t = sel["burned"] / 1000.0
        total = entry_t + land_t + RR_aux
        rows.append(dict(ok=True, mach=mach, entry_t=round(entry_t, 2),
                         land_t=round(land_t, 2), total_t=round(total, 2),
                         land_tl=sel["throttle"], h_ign=round(sel["h_ign"]),
                         v_cap=round(sel["v_final"], 2),
                         glide_vh=round(ge["vh"], 1), glide_v=round(ge["v"], 1),
                         x_km=round(ge["x"] / 1000.0, 1), ld=round(ld, 3),
                         cda=round(cda, 1)))
    oks = [r for r in rows if r["ok"]]
    out = dict(plan=plan, n=n, n_ok=len(oks),
               pct_chain_ok=round(100 * len(oks) / n, 1),
               reserve_t=reserve_t, corridor_mach=corridor,
               P_close_within_reserve=round(float(np.mean(
                   [r["total_t"] <= reserve_t for r in oks])), 3) if oks else 0.0,
               P_land_prop_le_nominal=None,
               exit_mach=stats([r["mach"] for r in oks], p=(5, 50, 95)) if oks else None,
               x_capture_km=stats([r["x_km"] for r in oks]) if oks else None,
               entry_prop_t=stats([r["entry_t"] for r in oks]) if oks else None,
               landing_prop_t=stats([r["land_t"] for r in oks], p=(50, 95, 99)) if oks else None,
               total_need_t=stats([r["total_t"] for r in oks], p=(50, 95, 99)) if oks else None,
               fail_modes={w: sum(1 for r in rows if not r["ok"] and r.get("why") == w)
                           for w in set(r.get("why") for r in rows if not r["ok"])},
               dispersion_assumptions="CD_A U(12,32) m2, L/D U(1.04,1.56), entry tl N(1,2.5%), "
                                      "Isp1 N(0,0.5 s); adaptive landing retarget")
    json.dump(rows, open(os.path.join(OUT, f"S11_samples_{plan}.json"), "w"))
    return out


RR_aux = 2.0   # aux allowance (same as R4)

if __name__ == "__main__":
    print("B5a — ascent MC (A x*, 400)...", flush=True)
    a = mc_ascent("A")
    print("B5a — ascent MC (B x*, 400)...", flush=True)
    b = mc_ascent("B")
    json.dump(dict(A=a, B=b), open(os.path.join(OUT, "S10_mc_ascent.json"), "w"), indent=1)
    for nm, o in (("A", a), ("B", b)):
        print(f"  {nm}: converged {o['n_converged']}/{o['n']}  deficit "
              f"{o['deficit']['mean']:.0f}+-{o['deficit']['sd']:.0f} "
              f"(p95 {o['deficit']['p95']:.0f})  P(q>35)={o['P_q_gt_35kpa']} "
              f"P(g>5)={o['P_g_gt_5']}")

    for pl in ("P0_documented", "P1_sized_M23"):
        print(f"B5b — recovery MC {pl} (500)...", flush=True)
        o = mc_recovery(pl)
        fn = "S11_mc_recovery.json"
        d = json.load(open(os.path.join(OUT, fn))) if os.path.exists(os.path.join(OUT, fn)) else {}
        d[pl] = o
        json.dump(d, open(os.path.join(OUT, fn), "w"), indent=1)
        print(f"  chain-ok {o['n_ok']}/{o['n']}; P(close within reserve)={o['P_close_within_reserve']}")
        if o["n_ok"]:
            print(f"  exit Mach {o['exit_mach']['mean']:.2f} [{o['exit_mach']['p5']:.2f},"
                  f"{o['exit_mach']['p95']:.2f}]  x_capture {o['x_capture_km']['mean']:.0f} km"
                  f" [{o['x_capture_km']['p5']:.0f},{o['x_capture_km']['p95']:.0f}]"
                  f"  total need p95 {o['total_need_t']['p95']:.1f} t")
        print(f"  fail modes: {o['fail_modes']}")
