"""
run_recovery.py — Day 7 Arc B4: recovery-chain studies (entry burn sizing,
terminal ignition window V-2, reserve closure R*, ship downrange solve V-4).
All inputs from OUR ascent model outputs (ALL_results.json), never copied
external values.  Results -> results/R*.json

v2 changes (Day 7 evening):
  * grid fins now verticalise the endgame (L/D taper 10 km -> 2 km) so the
    terminal hover-slam is genuinely near-vertical (model honesty fix);
  * terminal study uses the vertical component |vh| at taper-exit;
  * R4 fixed point damped (Rk <- Rk + 0.45*(Rnew-Rk)), landing feasibility
    tested on v_final <= V_CAPTURE, infeasible corridors flagged instead of
    crashing; landing-mass ceiling found by bisection for context.
"""
import json, math, os
import numpy as np
import params as P
import atmosphere as AT
import recovery_sim as RS

OUT = os.path.join(os.path.dirname(__file__), "results")
J = lambda n: json.load(open(os.path.join(OUT, n)))

# separation states from our ascent runs
ASC = J("ALL_results.json")
S0 = ASC["S0"]
SEP = dict(x=S0["meco_downrange_km"] * 1000, h=S0["meco_h_km"] * 1000,
           v=S0["meco_v"], gamma=math.radians(S0["meco_gamma_deg"]),
           m=RS.M_DRY_S1 + RS.M_RESV)
VX0 = SEP["v"] * math.cos(SEP["gamma"])
VH0 = SEP["v"] * math.sin(SEP["gamma"])
STATE0 = (0.0, SEP["x"], SEP["h"], VX0, VH0, SEP["m"])

ENTRY_H0, ENTRY_H1 = 70_000.0, 40_000.0     # entry-burn corridor (own design rule)
GLIDE_EXIT_H = RS.CAPTURE_H + 2_000.0       # terminal phase starts at 2,015 m


M_FLOOR = RS.M_DRY_S1          # entry/landing burns may only draw the reserve


def chain(m0, tl_entry, mach_exit_h=ENTRY_H1, ld=RS.LD_GLIDE,
          glide_exit_h=GLIDE_EXIT_H, record=True):
    """ballistic -> entry burn @ tl -> glide (L/D tapered). Returns rows, log, state."""
    return RS.integrate(
        (0.0, SEP["x"], SEP["h"], VX0, VH0, m0),
        [dict(kind="ballistic", exit_h=ENTRY_H0),
         dict(kind="entry_burn", n_eng=3, throttle=tl_entry, exit_h=mach_exit_h,
              m_floor=M_FLOOR),
         dict(kind="glide", LD=ld, exit_h=glide_exit_h)], record=record)


def _chain_candidate(m0, tl, exit_h=ENTRY_H1):
    """one scanned chain; returns (valid, eb, ge)."""
    rows, log, st = RS.integrate(
        (0.0, SEP["x"], SEP["h"], VX0, VH0, m0),
        [dict(kind="ballistic", exit_h=ENTRY_H0),
         dict(kind="entry_burn", n_eng=3, throttle=float(tl), exit_h=exit_h,
              m_floor=M_FLOOR),
         dict(kind="glide", LD=RS.LD_GLIDE, exit_h=GLIDE_EXIT_H)], record=False)
    eb, ge = log["entry_burn_exit"], log["glide_exit"]
    valid = (eb["m"] > M_FLOOR + 50.0          # burn did NOT hit the dry-mass floor
             and ge["h"] > -40.0               # did not impact before glide exit
             and st[0] < 3500.0)               # chain completed in sane time
    return valid, eb, ge


MACH_TOL = 0.08   # corridor match tolerance (tl scan resolution 0.01)


def entry_throttle_for_mach(m0, mach_target, exit_h=ENTRY_H1):
    """scan throttle, return (tl, mach, eb_log, ge_log) matching exit Mach within
    MACH_TOL among reserve-respecting candidates; (None, n_valid) if target
    is not reachable at this mass/reserve."""
    best = None
    n_valid = 0
    for tl in np.arange(0.40, 1.001, 0.01):
        valid, eb, ge = _chain_candidate(m0, float(tl), exit_h)
        if not valid:
            continue
        n_valid += 1
        mach = eb["v"] / AT.sound_speed(eb["h"])
        if abs(mach - mach_target) > MACH_TOL:
            continue
        if best is None or abs(mach - mach_target) < abs(best[1] - mach_target):
            best = (float(tl), mach, eb, ge)
    return best, n_valid


def landing_window(v_descent, h_start, m_start, reserve_avail_kg,
                   tls=(0.45, 0.55, 0.65, 0.70, 0.75, 0.85, 0.95, 1.00)):
    return RS.solve_hover_slam_ignition(v_descent, h_start, m_start,
                                        reserve_avail_kg, tls=tls)


def feasible_sol(win, v_tol=0.2):
    """feasible = reaches capture at <= V_CAPTURE; None if even tl=1.0 fails."""
    ok = [w for w in win if w["v_final"] <= RS.V_CAPTURE + v_tol]
    if not ok:
        return None
    return min(ok, key=lambda x: abs(x["throttle"] - 0.70))


# ------------------------------------------------------------------ R1 chain profile
def r1_baseline_chain():
    rows, log, st = chain(SEP["m"], 0.60)
    return dict(rows=rows, ballistic=log.get("ballistic_exit"),
                entry=log.get("entry_burn_exit"), glide=log.get("glide_exit"),
                vx_glide=None, final_m=st[5])


# ------------------------------------------------------------------ R2 entry sizing
def entry_metrics(mach_targets=(1.8, 2.0, 2.3, 2.7), m0=None):
    """Corridor-targeted sizing at fixed mass (default documented 58 t)."""
    m0 = SEP["m"] if m0 is None else m0
    out = []
    for mt in mach_targets:
        best, n_valid = entry_throttle_for_mach(m0, mt)
        if best is None:
            out.append(dict(mach_target=mt, feasible=False,
                            note="no throttle reaches exit within reserve"))
            continue
        tl, mach, eb, ge = best
        prop_used = (m0 - eb["m"]) / 1000.0
        dv = 300.0 * P.G0 * math.log(m0 / eb["m"])
        out.append(dict(mach_target=mt, throttle=round(tl, 2), feasible=True,
                        exit_mach=round(mach, 2), exit_v=round(eb["v"]),
                        entry_prop_t=round(prop_used, 1), entry_dv=round(dv),
                        glide_exit_v=round(ge["v"], 1), glide_exit_vh=round(ge["vh"], 1),
                        glide_x_km=round(ge["x"] / 1000, 0)))
    # what the documented reserve actually reaches: minimum-Mach valid candidate
    best_hot, hot_tl, hot_prop = None, None, None
    for tl in np.arange(0.40, 1.001, 0.01):
        valid, eb, ge = _chain_candidate(m0, float(tl))
        if not valid:
            continue
        mach = eb["v"] / AT.sound_speed(eb["h"])
        if best_hot is None or mach < best_hot:
            best_hot, hot_tl, hot_prop = mach, float(tl), (m0 - eb["m"]) / 1000.0
    out.append(dict(mach_target=None, feasible=True,
                    note="deepest corridor reachable at this mass within reserve",
                    exit_mach=round(best_hot, 2), throttle=round(hot_tl, 2),
                    entry_prop_t=round(hot_prop, 1)))
    return out


# ------------------------------------------------------------------ run everything
def run_all():
    results = {}

    print("R1 — baseline recovery chain (documented separation state, fins verticalise)")
    r1 = r1_baseline_chain()
    sepb, eb, ge = r1["ballistic"], r1["entry"], r1["glide"]
    vx_e = math.sqrt(max(eb["v"] ** 2 - eb["vh"] ** 2, 0.0))
    gam_b = math.degrees(math.atan2(sepb["vh"], math.sqrt(max(sepb["v"]**2 - sepb["vh"]**2, 1))))
    vx_g = math.sqrt(max(ge["v"] ** 2 - ge["vh"] ** 2, 0.0))
    gam_g = math.degrees(math.atan2(ge["vh"], max(vx_g, 1e-9)))
    print(f"  sep -> 70 km:  t={sepb['t']:.0f}s  x={sepb['x']/1000:.0f}km  "
          f"v={sepb['v']:.0f}m/s  vh={sepb['vh']:.0f}  gamma={gam_b:.1f}deg")
    print(f"  entry burn (3x60%) 70->40 km: prop={ (STATE0[5]-eb['m'])/1000:.1f} t, "
          f"exit v={eb['v']:.0f} m/s (Mach {eb['v']/AT.sound_speed(eb['h']):.1f})")
    print(f"  glide exit (2,015 m): x={ge['x']/1000:.0f} km, v={ge['v']:.0f} m/s, "
          f"vh={ge['vh']:.0f}, vx={vx_g:.0f} (gamma {gam_g:.0f} deg)")
    r1_out = dict(ballistic=sepb, entry=eb, glide=ge, gamma_at_70km=round(gam_b, 1),
                  gamma_glide_exit=round(gam_g, 1))
    json.dump(r1_out, open(os.path.join(OUT, "R1_chain.json"), "w"), indent=1)
    json.dump([[round(a, 1) if not isinstance(a, str) else a for a in r]
               for r in r1["rows"][::10]],
              open(os.path.join(OUT, "R1_profile.json"), "w"))

    print("\nR2 — corridor-targeted entry sizing (3 engines, exit at 40 km, 58 t documented)")
    r2 = entry_metrics()
    for row in r2:
        if row["mach_target"] is None:
            print(f"  deepest reachable at documented reserve: M{row['exit_mach']} "
                  f"(tl {row['throttle']:.2f}, prop {row['entry_prop_t']:.1f} t)")
            continue
        if not row.get("feasible", True):
            print(f"  exit Mach {row['mach_target']}: {row['note']} -> INFEASIBLE at 58 t/18 t reserve")
            continue
        print(f"  exit Mach {row['mach_target']}: tl {row['throttle']:.2f} (got M{row['exit_mach']})  "
              f"prop {row['entry_prop_t']:4.1f} t (dv {row['entry_dv']:4.0f})  "
              f"glide-exit v {row['glide_exit_v']:.0f} m/s vh {row['glide_exit_vh']:.0f}")
    json.dump(r2, open(os.path.join(OUT, "R2_entry_sizing.json"), "w"), indent=1)
    results["R2"] = r2

    print("\nR3 — terminal ignition window (V-2), tapered-glide exit at 2,015 m")
    v0 = abs(ge["vh"]); h0 = ge["h"]; m3 = eb["m"]
    win = landing_window(v0, h0, m3, RS.M_RESV)
    for w in win:
        print(f"  tl={w['throttle']:.2f}: ignite h={w['h_ign']:6.0f} m -> v_cap {w['v_final']:4.1f} m/s "
              f"(burn {w['t_burn']:.1f}s, {w['burned']/1000:.2f} t)")
    sel = feasible_sol(win)
    win_c = landing_window(abs(ge["v"]), h0, m3, RS.M_RESV)   # conservative: kill full |v|
    sel_c = feasible_sol(win_c)
    print(f"  selected (near tl 0.70): h_ign={sel['h_ign']:.0f} m, landing prop {sel['burned']/1000:.2f} t")
    print(f"  conservative (kill full |v|={ge['v']:.0f}): h_ign={sel_c['h_ign']:.0f} m, "
          f"prop {sel_c['burned']/1000:.2f} t at tl {sel_c['throttle']:.2f}")
    json.dump(dict(glide_exit=dict(v=ge["v"], vh=ge["vh"], h=ge["h"], m=m3,
                                   gamma_deg=round(gam_g, 1)),
                   window=win, selected=sel,
                   window_conservative=win_c, selected_conservative=sel_c),
              open(os.path.join(OUT, "R3_terminal_window.json"), "w"), indent=1)
    results["R3"] = dict(selected_burned_t=sel["burned"] / 1000.0,
                         selected_h_ign=sel["h_ign"])

    print("\nR4 — recovery reserve closure: grid scan for R s.t. need(R) <= R (fixed point)")
    aux = 2.0   # RCS/settle ~1 t + flight margin ~1 t (own estimates)

    def need_at_R(mt, Rk):
        """total reserve need at assumed reserve Rk; None + reason if infeasible."""
        m_sep = RS.M_DRY_S1 + Rk * 1000.0
        best, n_valid = entry_throttle_for_mach(m_sep, mt)
        if best is None:
            return None, "entry corridor unreachable within reserve", None
        tl, mach, ebx, gex = best
        pe = (m_sep - ebx["m"]) / 1000.0
        if pe >= Rk:
            return None, "entry burn alone exceeds reserve", None
        w = landing_window(abs(gex["vh"]), gex["h"], ebx["m"], Rk * 1000.0 - pe * 1000.0)
        selx = feasible_sol(w)
        if selx is None:
            return None, "landing infeasible at tl<=1.0", None
        pl = selx["burned"] / 1000.0
        return pe + pl + aux, "ok", dict(entry_t=pe, landing_t=pl, entry_tl=tl,
                                         landing_tl=selx["throttle"], h_ign_m=selx["h_ign"])

    R_hist = {}
    for mt in (1.8, 2.0, 2.3, 2.7):
        trace = []
        for Rk in np.arange(12.0, 46.01, 2.0):
            need, why, det = need_at_R(mt, float(Rk))
            trace.append((round(float(Rk), 1),
                          round(need, 1) if need else None, why))
        Rstar = None
        for Rk, need, why in trace:
            if need is not None and need <= Rk:
                # refine around crossing at 0.2 t
                for Rf in np.arange(Rk - 2.0, Rk + 0.01, 0.2):
                    nf, whyf, detf = need_at_R(mt, float(Rf))
                    if nf is not None and nf <= Rf:
                        Rstar = (round(float(Rf), 1), nf, detf)
                        break
                if Rstar is None:
                    Rstar = (float(Rk), need, det)
                break
        # also: need at the documented 18 t reserve
        n18, why18, _ = need_at_R(mt, 18.0)
        if Rstar:
            Rk, need, det = Rstar
            R_hist[f"M{mt}"] = dict(R_star_t=Rk, need_at_Rstar_t=round(need, 1),
                                    need_at_18t_t=(round(n18, 1) if n18 else None),
                                    note_at_18t=(None if n18 else why18), **det, aux_t=aux)
            print(f"  corridor Mach {mt}: R* = {Rk:5.1f} t (entry {det['entry_t']:.1f} tl {det['entry_tl']:.2f}"
                  f" + landing {det['landing_t']:.1f} tl {det['landing_tl']:.2f} + aux 2.0)"
                  f"   | at documented 18 t: {'need ' + format(n18, '.1f') + ' t' if n18 else why18}")
        else:
            R_hist[f"M{mt}"] = dict(R_star_t=None,
                                    need_at_18t_t=(round(n18, 1) if n18 else None),
                                    note_at_18t=(None if n18 else why18),
                                    status="no closure: corridor unreachable or landing-infeasible for R in [12,46] t",
                                    trace=trace)
            n_ok = [t_ for t_ in trace if t_[1] is not None]
            print(f"  corridor Mach {mt}: NO CLOSURE in R in [12,46] t"
                  f"   | at documented 18 t: {'need ' + format(n18, '.1f') + ' t' if n18 else why18}")
            if n_ok:
                print(f"      (needs computed up to R={n_ok[-1][0]:.0f} t still exceed R: {n_ok[-1][1]:.0f} t)")
    feas = [v["R_star_t"] for v in R_hist.values() if v.get("R_star_t")]
    if feas:
        verdict = (f"documented 18 t reserve reaches only ~Mach 2.9 at 40 km (hotter than the "
                   f"anchored reusable-family corridor Mach 1.8-2.7); closing credible corridors "
                   f"needs R* = {min(feas):.0f}-{max(feas):.0f} t. "
                   f"Day-4 recovery reserve (18 t) is undersized ~2x; "
                   f"Day-6 hybrid-vs-legged 6 t reserve saving is not supported (need >= legged 24 t).")
    else:
        verdict = "no corridor closes within R in [12,46] t -> recovery architecture must change"
    closure = dict(corridors=R_hist, aux_t=aux,
                   documented_reserve_t=P.M_S1_RESV / 1000.0, documented_legged_t=24.0,
                   verdict=verdict)
    print("  verdict:", verdict)
    json.dump(closure, open(os.path.join(OUT, "R4_closure.json"), "w"), indent=1)
    results["R4"] = closure

    print("\nR5 — ship downrange solve (V-4 preliminary, tapered fins)")
    sens = []
    hot = [r for r in r2 if r["mach_target"] is None][0]
    tl_ship = hot["throttle"]   # entry plan the documented reserve can actually fly
    print(f"  (using deepest reachable corridor at documented reserve: "
          f"M{hot['exit_mach']} at tl {hot['throttle']:.2f})")
    for ld in (1.0, 1.3, 1.6):
        rowsx, logx, stx = chain(SEP["m"], tl_ship, ld=ld)
        g = logx["glide_exit"]
        sens.append(dict(LD=ld, x_capture_km=round(g["x"] / 1000),
                         v_exit=round(g["v"], 1), vh_exit=round(g["vh"], 1)))
        print(f"  L/D={ld}: capture-zone entry at x={g['x']/1000:.0f} km "
              f"(v {g['v']:.0f} m/s, vh {g['vh']:.0f})")
    base_x = [s for s in sens if s["LD"] == 1.3][0]["x_capture_km"]
    ship = dict(x_ship_center_km=base_x,
                corridor_km=[min(s["x_capture_km"] for s in sens),
                             max(s["x_capture_km"] for s in sens)],
                corridor_width_km=max(s["x_capture_km"] for s in sens) - min(s["x_capture_km"] for s in sens),
                note="ship = corridor centre; grid-fin L/D +/-20% drives corridor spread; "
                     "separation point moves with Day-8 architecture choice -> re-solve then")
    print(f"  ship centre ~ {base_x} km, corridor {ship['corridor_km']} "
          f"(width {ship['corridor_width_km']} km)")
    json.dump(dict(sens=sens, ship=ship), open(os.path.join(OUT, "R5_ship.json"), "w"), indent=1)
    results["R5"] = ship

    json.dump(results, open(os.path.join(OUT, "R_all.json"), "w"), indent=1)
    return results


if __name__ == "__main__":
    run_all()
