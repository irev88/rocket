"""
tune_kick.py — calibrate the S1 pitch-kick angle so the honest model
reproduces the Day-5 master-data S1 segment (gate G3 anchor points).
Only the pitch program is tuned; all physics stays untouched.
"""
import math
import params as P
import sim


def score(kick_deg, verbose=False):
    cfg = sim.Config(pitch_kick=math.radians(kick_deg),
                     jettison_fairing=False, q_limit=None,
                     label=f"kick{kick_deg:.1f}")
    res = sim.run(cfg, record_dt=5.0)
    meco = res["events"]["MECO"]
    # master-data anchors: (t, h, v)
    anchors = [(60, 9300, 420), (90, 24000, 1150), (120, 40000, 2030),
               (140, 61000, 2410), (150, 78000, 2520)]
    err = 0.0
    got = {}
    for ta, ha, va in anchors:
        row = min(res["rows"], key=lambda r: abs(r[0] - ta))
        got[ta] = (row[2], row[3])
        err += abs(row[2] - ha) / ha + abs(row[3] - va) / va
    # MECO target: 150 s / 78 km / 2520 m/s
    err += abs(meco["t"] - 150) / 150 + abs(meco["h"] - 78000) / 78000 + abs(meco["v"] - 2520) / 2520
    if verbose:
        print(f" kick={kick_deg:5.2f}° err={err:6.3f}  MECO t={meco['t']:6.1f} h={meco['h']/1000:6.1f} "
              f"v={meco['v']:6.0f} γ={meco['gamma']:5.1f}°")
        for ta, ha, va in anchors:
            gh, gv = got[ta]
            print(f"   t={ta:4d}: h {gh:9.0f} vs {ha:7.0f} ({(gh-ha)/ha*100:+5.1f}%)   "
                  f"v {gv:7.1f} vs {va:6.0f} ({(gv-va)/va*100:+5.1f}%)")
    return err, res


if __name__ == "__main__":
    best = None
    for kd in [6, 8, 10, 12, 14, 16, 18, 20, 22]:
        e, _ = score(kd, verbose=True)
        if best is None or e < best[0]:
            best = (e, kd)
    print(f"\n coarse best: {best[1]:.1f}°  err={best[0]:.3f}")
    fine = None
    for kd in [best[1] + d for d in (-2, -1, -0.5, 0, 0.5, 1, 2)]:
        e, _ = score(kd, verbose=True)
        if fine is None or e < fine[0]:
            fine = (e, kd)
    print(f"\n fine best: {fine[1]:.2f}°  err={fine[0]:.3f}")
    score(fine[1], verbose=True)
