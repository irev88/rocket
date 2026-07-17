"""
studies.py — Day 7 repair studies, clean deterministic suite.

Guidance-tuning policy: each candidate design point is evaluated at the best
member of a guidance grid matched to its engine class:
  * 1x MVac (T/W 0.66): strong loft bias schedules + kick 3.5 deg (only
    survivable S1 program for this T/W class within our guidance family)
  * 2x MVac (T/W 1.3): near-prograde + kick grid 3.5-6.0 deg
This emulates per-point trajectory optimization inside our guidance family;
full joint optimization (collocation/PEG) is flagged as follow-on work (B3).

Outputs: results/*.json
"""
import json, math, os
import params as P
import sim

OUT = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(OUT, exist_ok=True)

GRID_1X = [(b, h) for b, h in ((14, 220), (18, 240), (18, 200), (22, 260),
                               (22, 220), (26, 300), (26, 260))]
GRID_2X = [(b, h) for b, h in ((0, 200), (2, 200), (4, 200), (6, 200),
                               (6, 260), (10, 220), (10, 260), (14, 220),
                               (18, 240), (22, 260))]
KICK_1X = [3.5]
KICK_2X = [3.5, 4.0, 4.5, 5.0, 5.5, 6.0]


def tune(base_kwargs):
    n2 = base_kwargs.get("n_eng_s2", 1)
    grid = GRID_1X if n2 == 1 else GRID_2X
    kicks = KICK_1X if n2 == 1 else KICK_2X
    pool, pool_valid = [], []
    for kick in kicks:
        for b0, hold in grid:
            kw = dict(base_kwargs,
                      pitch_kick=math.radians(kick), t_kick0=12.0, t_kick1=30.0,
                      s2_guidance="schedule", s2_bias0=math.radians(b0),
                      s2_bias_hold=hold, jettison_fairing=True, kick=kick)
            cfg = sim.Config(**kw)
            res = sim.run(cfg, record_dt=2.0)
            if "SECO" not in res["events"] or res["orbit"] is None:
                continue
            d = res["deficit_to_500x500"]
            if d is None or math.isnan(d):
                continue
            res["guidance"] = dict(kick_deg=kick, bias0_deg=b0, hold_s=hold)
            pool.append(res)
            meco = res["events"]["MECO"]
            if meco["h"] >= 50_000 and res["q_max"] <= P.Q_STRUCT * 1.03:
                pool_valid.append(res)
    use = pool_valid or pool
    return min(use, key=lambda r: r["deficit_to_500x500"]) if use else None


def brief(res):
    ev = res["events"]; meco, seco = ev["MECO"], ev["SECO"]
    orb = res["orbit"]
    cfg = res["cfg"]
    return dict(
        label=cfg.label, glom_t=round(cfg.glom / 1000, 3),
        n_eng_s2=cfg.n_eng_s2,
        t_meco=round(meco["t"], 1), meco_h_km=round(meco["h"] / 1000, 2),
        meco_v=round(meco["v"], 1), meco_gamma_deg=round(meco["gamma"], 2),
        meco_mach=round(meco["mach"], 2), meco_downrange_km=round(meco["x"] / 1000, 1),
        m_drop_kg=round(cfg.s1_drop, 0),
        t_seco=round(seco["t"], 1), seco_h_km=round(seco["h"] / 1000, 1),
        seco_v=round(seco["v"], 1), seco_gamma_deg=round(seco["gamma"], 2),
        apogee_km=round(orb["apogee_km"], 0), perigee_km=round(orb["perigee_km"], 0),
        deficit_m_s=round(res["deficit_to_500x500"], 0),
        q_max_kpa=round(res["q_max"] / 1000, 2), q_max_s1_kpa=round(res["q_max_s1"] / 1000, 2),
        q_max_t=round(res["q_max_t"], 1), q_max_h_km=round(res["q_max_h"] / 1000, 2),
        q_max_mach=round(res["q_max_mach"], 2),
        struct_valid=bool(res["q_max"] <= P.Q_STRUCT),
        isp_avg_s1=round(sim.effective_avg_isp(res, 1), 1),
        isp_avg_s2=round(sim.effective_avg_isp(res, 2), 1),
        dv_thrust_s1=round(res["losses"]["I_thrust_s1"], 0),
        dv_thrust_s2=round(res["losses"]["I_thrust_s2"], 0),
        dv_grav_s1=round(res["losses"]["I_grav_s1"], 0),
        dv_grav_s2=round(res["losses"]["I_grav_s2"], 0),
        dv_drag=round(res["losses"]["I_drag"], 0),
        dv_steer=round(res["losses"]["I_steer"], 0),
        m_final_kg=round(res["m_final"], 0),
        g_max=round(res["g_max"], 2),
        tsio_s2_ideal=round(cfg.tsiolkovsky_s2, 0),
        guidance=res.get("guidance"),
        feasible=True,
    )


def save(name, obj):
    with open(os.path.join(OUT, name), "w") as f:
        json.dump(obj, f, indent=1)
    print("  wrote", name)


def s2_stack_tw(p2, pl=20e3, margin=7e3, n2=1):
    stack = pl + 600 + 1800 + 5500 + (550 if n2 == 2 else 0) + p2 + 2500 + 1600 + margin
    return n2 * P.THR2_VAC / (stack * P.G0)


def run_all_studies():
    results = {}

    # ------------------------------------------------------------- S0 baseline
    print("STUDY 0 — honest baseline at documented masses (1x MVac)")
    base = tune(dict(m_s1_prop=391e3, m_s2_prop=112e3, m_payload=20e3,
                     label="S0_baseline"))
    save("S0_baseline.json", brief(base)); results["S0"] = brief(base)
    b = brief(base)
    print(f"  MECO {b['t_meco']:.0f}s {b['meco_h_km']:.1f}km {b['meco_v']:.0f}m/s g{b['meco_gamma_deg']:.1f} | "
          f"deficit {b['deficit_m_s']:.0f} m/s | Q {b['q_max_kpa']:.1f} kPa @{b['q_max_t']:.0f}s")

    # ------------------------------------------------- audit re-derivation
    L = base["losses"]
    old = dict(
        s1_implied_isp=round((2520.0 + L["I_grav_s1"] + L["I_drag_s1"])
                             / (P.G0 * math.log(600000.0 / 209000.0)), 0),
        s2_implied_isp=round(((7610.0 - 2530.0) + L["I_grav_s2"] + L["I_drag_s2"])
                             / (P.G0 * math.log(151000.0 / 39000.0)), 0),
        envelope_s1="282–311 s", declared_s2="348 s",
        note="implied Isp = (old velocity gain + honest losses proxy) / (g0*ln(ratio)); "
             ">vacuum Isp proves energy non-conservation (audit C-1 re-derived)")
    save("S0_audit_implied_isp.json", old)
    print(f"  old-data implied Isp: S1 {old['s1_implied_isp']:.0f}s (env 282–311), "
          f"S2 {old['s2_implied_isp']:.0f}s (decl 348)  => C-1 re-derived")

    # ------------------------------------------------------------- S1 bucket
    print("STUDY 1 — Max-Q throttle bucket (baseline config)")
    rows = []
    for qlim, tag in ((None, "no_bucket"), (35e3, "35kPa"), (30e3, "30kPa"), (28e3, "28kPa")):
        r = tune(dict(m_s1_prop=391e3, m_s2_prop=112e3, m_payload=20e3,
                      q_limit=qlim, label=f"S1_{tag}"))
        b = brief(r); b["q_limit"] = tag; rows.append(b)
        print(f"  {tag:>10}: Qmax(S1) {b['q_max_s1_kpa']:5.1f} kPa  MECO {b['meco_h_km']:5.1f}km/"
              f"{b['meco_v']:5.0f}m/s  deficit {b['deficit_m_s']:5.0f}")
    save("S1_bucket.json", rows); results["S1"] = rows

    # --------------------------------------------- S2 split feasibility bound
    print("STUDY 2 — propellant-split feasibility boundary (GLOM 600 t, 20 t payload, 1x MVac)")
    rows = []
    for p1 in (391e3, 388e3, 385e3, 382e3, 378e3, 370e3):
        p2 = 503e3 - p1
        r = tune(dict(m_s1_prop=p1, m_s2_prop=p2, m_payload=20e3,
                      label=f"S2_P1_{p1/1000:.0f}t"))
        if r is None:
            rows.append(dict(p1_t=p1/1000, p2_t=p2/1000, feasible=False,
                             s2_tw_ign=round(s2_stack_tw(p2), 3), deficit_m_s=None))
            print(f"  P1 {p1/1000:4.0f}/P2 {p2/1000:4.0f} T/W={s2_stack_tw(p2):.2f}: CRASH (infeasible)")
            continue
        b = brief(r); b.update(p1_t=p1/1000, p2_t=p2/1000,
                               s2_tw_ign=round(s2_stack_tw(p2), 3)); rows.append(b)
        print(f"  P1 {p1/1000:4.0f}/P2 {p2/1000:4.0f} T/W={s2_stack_tw(p2):.2f}: deficit {b['deficit_m_s']:5.0f}"
              f"  valid={b['struct_valid']}")
    save("S2_split.json", rows); results["S2"] = rows

    # ------------------------------------------------ S3 payload capability
    print("STUDY 3 — payload capability at 600 t GLOM reusable (1x MVac)")
    rows = []
    for tag, kw in (("doc391", dict(m_s1_prop=391e3, m_s2_prop=112e3)),
                    ("margin2prop", dict(m_s1_prop=391e3, m_s2_prop=119e3, m_margin=0.0))):
        for pl in (3e3, 4e3, 5e3, 6e3, 8e3, 10e3, 12e3, 14e3, 16e3, 20e3):
            r = tune(dict(m_payload=pl, label=f"S3_{tag}_{pl/1000:.0f}t", **kw))
            if r is None:
                print(f"  {tag:>11} {pl/1000:4.0f} t: INFEASIBLE")
                continue
            b = brief(r); b.update(payload_t=pl/1000, variant=tag); rows.append(b)
            print(f"  {tag:>11} {pl/1000:4.0f} t: deficit {b['deficit_m_s']:6.0f}")
    save("S3_payload.json", rows); results["S3"] = rows

    # ------------------------------------------------ S4 expendable (1x MVac)
    print("STUDY 4 — expendable conversion (1x MVac, reserve as ascent prop, HW removed)")
    rows = []
    for tag, kw in (("exp", dict(m_s2_prop=112e3)),
                    ("exp+m2p", dict(m_s2_prop=119e3, m_margin=0.0))):
        for pl in (8e3, 10e3, 12e3, 14e3, 16e3, 20e3):
            r = tune(dict(m_s1_dry=P.M_S1_STRUCT + P.M_S1_ENG,
                          m_s1_resv=0.0, m_s1_prop=409e3,
                          m_payload=pl, label=f"S4_{tag}_{pl/1000:.0f}t", **kw))
            if r is None:
                print(f"  {tag:>8} {pl/1000:4.0f} t: INFEASIBLE")
                continue
            b = brief(r); b.update(payload_t=pl/1000, variant=tag); rows.append(b)
            print(f"  {tag:>8} {pl/1000:4.0f} t: deficit {b['deficit_m_s']:6.0f}")
    save("S4_expendable.json", rows); results["S4"] = rows

    # --------------------------------------------- S5 1x MVac growth barrier
    print("STUDY 5 — growth via S2 prop only (1x MVac): T/W barrier")
    rows = []
    for add in (30e3, 60e3, 90e3, 120e3):
        r = tune(dict(m_s1_prop=391e3, m_s2_prop=112e3 + add, m_payload=20e3,
                      label=f"S5_add{add/1000:.0f}t"))
        tw = s2_stack_tw(112e3 + add)
        if r is None:
            rows.append(dict(add_t=add/1000, tw=round(tw, 3), feasible=False, deficit_m_s=None))
            print(f"  +{add/1000:4.0f} t (T/W={tw:.2f}): INFEASIBLE")
            continue
        b = brief(r); b.update(add_t=add/1000, tw=round(tw, 3)); rows.append(b)
        print(f"  +{add/1000:4.0f} t (T/W={tw:.2f}): deficit {b['deficit_m_s']:6.0f}")
    save("S5_growth_1mvac.json", rows); results["S5"] = rows

    # --------------------------------------------- S6 second-MVac iteration
    print("STUDY 6 — architecture iteration: 2nd MVac (+550 kg S2 dry)")
    kw2 = dict(n_eng_s2=2, m_s2_dry=P.M_S2_DRY + 550.0)
    rows = []
    # 6a: 600 t, 20 t payload, margin2prop variants
    for tag, kw in (("2xMVac_600t_20t", dict(m_s2_prop=112e3)),
                    ("2xMVac_600t_20t_m2p", dict(m_s2_prop=119e3, m_margin=0.0))):
        r = tune(dict(m_s1_prop=391e3, m_payload=20e3, label=tag, **{**kw2, **kw}))
        b = brief(r) if r else None
        if b:
            rows.append(b)
            print(f"  {tag:>22}: deficit {b['deficit_m_s']:6.0f}  Q {b['q_max_kpa']:4.1f}  "
                  f"MECO {b['meco_h_km']:5.1f}km v{b['meco_v']:5.0f} g{b['meco_gamma_deg']:4.1f}")
    save("S6_2mvac_600t.json", rows); results["S6a"] = rows

    # 6b: closure growth with 2x MVac (+margin converted)
    print("STUDY 6b — GLOM growth to close 20 t SSO (2x MVac, margin converted)")
    lo, hi, bestrow = 0.0, 120e3, None
    for _ in range(16):
        mid = 0.5 * (lo + hi)
        r = tune(dict(m_s1_prop=391e3, m_s2_prop=119e3 + mid, m_margin=0.0,
                      m_payload=20e3, label=f"S6b_add{mid/1000:.1f}t", **kw2))
        d = r["deficit_to_500x500"] if r else 1e9
        if d > 20.0:
            lo = mid
        else:
            hi = mid; bestrow = r
    if bestrow:
        b = brief(bestrow); save("S6b_closure.json", b); results["S6b"] = b
        print(f"  closure: +{(bestrow['cfg'].glom-600e3)/1000:5.1f} t -> GLOM {bestrow['cfg'].glom/1000:6.1f} t, "
              f"deficit {b['deficit_m_s']:4.0f}")
    else:
        print("  no closure up to +120 t")

    # 6c: expendable + 2x MVac closure payload at 600 t
    print("STUDY 6c — expendable 2x MVac, payload sweep at 600 t")
    rows = []
    for pl in (14e3, 16e3, 20e3, 24e3):
        r = tune(dict(m_s1_dry=P.M_S1_STRUCT + P.M_S1_ENG, m_s1_resv=0.0,
                      m_s1_prop=409e3, m_s2_prop=119e3, m_margin=0.0,
                      m_payload=pl, label=f"S6c_exp2x_PL{pl/1000:.0f}t", **kw2))
        if r is None:
            print(f"  PL {pl/1000:4.0f}: INFEASIBLE")
            continue
        b = brief(r); b.update(payload_t=pl/1000); rows.append(b)
        print(f"  PL {pl/1000:4.0f} t: deficit {b['deficit_m_s']:6.0f}")
    save("S6c_exp2x_payload.json", rows); results["S6c"] = rows

    # 6d: scaled family closure (12x M1D + 4x MVac, prop scale factor f)
    print("STUDY 6d — scaled-architecture closure probe (12x M1D + 4x MVac)")
    KICKS_D = (1.5, 2.0, 2.5, 3.0, 3.5, 4.0)
    BIAS_D  = ((0, 200), (2, 200), (4, 220), (6, 220), (8, 240), (10, 240), (14, 260))
    def probe_f(f):
        best = None
        for kick in KICKS_D:
            for b0, hold in BIAS_D:
                kw = dict(pitch_kick=math.radians(kick), t_kick0=12, t_kick1=30,
                          s2_guidance="schedule", s2_bias0=math.radians(b0),
                          s2_bias_hold=hold, jettison_fairing=True,
                          m_s1_prop=391e3 * f, m_s2_prop=119e3 * f, m_margin=0.0,
                          m_payload=20e3, n_eng_s1=12, n_eng_s2=4,
                          m_s1_dry=(P.M_S1_STRUCT + P.M_S1_ENG + P.M_REC_HW) * (12/9)**0.8,
                          m_s2_dry=P.M_S2_DRY + 550.0 * 3,
                          label=f"S6d_f{f:.2f}")
                r = sim.run(sim.Config(**kw), record_dt=2.0)
                if "SECO" not in r["events"] or r["orbit"] is None:
                    continue
                if r["events"]["MECO"]["h"] < 40_000 or r["q_max"] > P.Q_STRUCT * 1.05:
                    continue
                d = r["deficit_to_500x500"]
                if best is None or d < best["deficit_to_500x500"]:
                    best = r
                    best["guidance"] = dict(kick_deg=kick, bias0_deg=b0, hold_s=hold)
        return best
    rows = []
    fpts = {}
    for f in (1.30, 1.35, 1.40, 1.45):
        r = probe_f(f)
        if r is None:
            print(f"  f={f:.2f}: no valid run")
            continue
        b = brief(r); b["f"] = f; rows.append(b); fpts[f] = b["deficit_m_s"]
        print(f"  f={f:.2f} GLOM {b['glom_t']:6.1f}: deficit {b['deficit_m_s']:7.0f}")
    save("S6d_scaled_family.json", rows); results["S6d"] = rows
    # closure interpolation
    fs = sorted(fpts)
    f_close = None
    for f1, f2 in zip(fs, fs[1:]):
        if fpts[f1] > 0 >= fpts[f2]:
            f_close = f1 + (f2 - f1) * fpts[f1] / (fpts[f1] - fpts[f2])
    if f_close:
        g_close = 600.5 + 510 * (f_close - 1)
        closure = dict(f_close=round(f_close, 3), glom_kg=round(g_close * 1000, 0),
                       note="linear interpolation between verified sim points; "
                            "deficit<0 = braking margin on target-circle arrival")
        save("S6d_closure_estimate.json", closure); results["S6d_close"] = closure
        print(f"  closure at f≈{f_close:.2f} -> GLOM≈{g_close:,.0f} t")

    save("ALL_results.json", results)
    return results


if __name__ == "__main__":
    run_all_studies()
