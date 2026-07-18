"""
plots.py — Day 7 figure generation into results/fig*_*.png
"""
import json, math, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import params as P
import sim

OUT = os.path.join(os.path.dirname(__file__), "results")
J = lambda n: json.load(open(os.path.join(OUT, n)))

plt.rcParams.update({"font.size": 10, "axes.grid": True, "grid.alpha": 0.3,
                     "figure.dpi": 130})
NAVY, ORANGE, GREEN, RED, GRAY = "#16324F", "#E0561E", "#1E7A46", "#B3271E", "#6B7280"


def run_cfg(**kw):
    cfg = sim.Config(**kw)
    return sim.run(cfg, record_dt=1.0)


# ------------------------------------------------------------------ fig 1
def fig1():
    base = J("S0_baseline.json")
    g = base["guidance"]
    res = run_cfg(pitch_kick=math.radians(g["kick_deg"]), t_kick0=12, t_kick1=30,
                  s2_guidance="schedule", s2_bias0=math.radians(g["bias0_deg"]),
                  s2_bias_hold=g["hold_s"], jettison_fairing=True)
    t_seco = res["events"]["SECO"]["t"]
    rows = [r for r in res["rows"] if r[0] <= t_seco]     # crop disposal dive
    t = [r[0] for r in rows]
    h = [r[2] / 1000 for r in rows]
    v = [r[3] for r in rows]
    q = [r[6] / 1000 for r in rows]
    m = [r[7] / 1000 for r in rows]
    mt = [r[0] for r in P.MASTER]
    mh = [r[1] / 1000 for r in P.MASTER]
    mv = [r[2] for r in P.MASTER]
    mm = [r[5] / 1000 for r in P.MASTER]

    fig, ax = plt.subplots(2, 2, figsize=(11, 6.5))
    fig.suptitle("Day 7 honest baseline vs Day 5 master data (documented masses)")
    ax[0, 0].plot(t, h, color=NAVY, lw=1.8, label="Day 7 (honest)")
    ax[0, 0].plot(mt, mh, "o", color=ORANGE, ms=3.5, label="Day 5 master data")
    ax[0, 0].set_ylabel("altitude (km)"); ax[0, 0].legend(fontsize=8)
    ax[0, 1].plot(t, v, color=NAVY, lw=1.8)
    ax[0, 1].plot(mt, mv, "o", color=ORANGE, ms=3.5)
    ax[0, 1].axhline(7612, color=GREEN, ls="--", lw=1, label="500 km circular (7,612 m/s)")
    ax[0, 1].set_ylabel("velocity (m/s)"); ax[0, 1].legend(fontsize=8)
    ax[1, 0].plot(t, q, color=NAVY, lw=1.8)
    ax[1, 0].scatter([res["q_max_t"]], [res["q_max"] / 1000], color=RED, zorder=5,
                     label=f"Max-Q {res['q_max']/1000:.1f} kPa @ t+{res['q_max_t']:.0f}s")
    ax[1, 0].scatter([60], [40.4], color=ORANGE, zorder=5, marker="s",
                     label="Day 5 own data: 40.4 kPa @ t+60s")
    ax[1, 0].set_ylabel("dyn. pressure (kPa)"); ax[1, 0].set_xlabel("t (s)"); ax[1, 0].legend(fontsize=8)
    ax[1, 1].plot(t, m, color=NAVY, lw=1.8)
    ax[1, 1].plot(mt, mm, "o", color=ORANGE, ms=3.5)
    ax[1, 1].set_ylabel("mass (t)"); ax[1, 1].set_xlabel("t (s)")
    for a in ax.flat:
        a.set_xlim(0, 560)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(os.path.join(OUT, "fig1_profile.png")); plt.close(fig)
    print("fig1_profile.png")


# ------------------------------------------------------------------ fig 2
def fig2():
    b = J("S0_baseline.json")
    ideal_s1 = b["dv_thrust_s1"]            # computed from honest Isp integral
    ideal_s2 = b["tsio_s2_ideal"]
    grav_s1, grav_s2 = b["dv_grav_s1"], b["dv_grav_s2"]
    drag, steer = b["dv_drag"], b["dv_steer"]
    vfin, deficit = b["seco_v"], b["deficit_m_s"]

    labels = ["Recorded\nrequirement\n(Day 2)", "Honest ideal\nS1+S2", "gravity\n", "drag +\nsteering",
              "net speed\nat SECO", "deficit to\n500×500", "500 km SSO\ncircular"]
    fig, ax = plt.subplots(figsize=(10.5, 5.2))
    ax.set_title("Δv accounting — why 11.0 km/s vs. honest capability is the real story")
    x = range(len(labels))
    # bar 1: recorded requirement
    ax.bar(0, 11000, color=GRAY, alpha=0.85)
    ax.text(0, 11000 + 80, "11,000", ha="center", fontsize=9)
    # bar 2: honest ideal
    ax.bar(1, ideal_s1 + ideal_s2, color=NAVY)
    ax.text(1, ideal_s1 + ideal_s2 + 80, f"{ideal_s1+ideal_s2:,.0f}", ha="center", fontsize=9)
    # waterfall: ideal -> minus grav -> minus drag/steer -> net
    ax.bar(2, -grav_s1 - grav_s2, bottom=ideal_s1 + ideal_s2, color=ORANGE)
    ax.text(2, ideal_s1 + ideal_s2 - grav_s1 - grav_s2 - 260, f"−{grav_s1+grav_s2:,.0f}", ha="center", fontsize=9)
    ax.bar(3, -drag - steer, bottom=ideal_s1 + ideal_s2 - grav_s1 - grav_s2, color="#E8A33D")
    ax.text(3, ideal_s1 + ideal_s2 - grav_s1 - grav_s2 - drag - steer - 260, f"−{drag+steer:,.0f}", ha="center", fontsize=9)
    ax.bar(4, vfin, color=GREEN)
    ax.text(4, vfin + 80, f"{vfin:,.0f}", ha="center", fontsize=9)
    ax.bar(5, deficit, bottom=vfin, color=RED, alpha=0.8)
    ax.text(5, vfin + deficit + 80, f"+{deficit:,.0f}", ha="center", fontsize=9)
    ax.axhline(7612, color=GREEN, ls="--", lw=1.2)
    ax.text(6.0, 7612 + 90, "7,612", fontsize=9, color=GREEN)
    ax.set_xticks(list(x)); ax.set_xticklabels(labels, fontsize=8.5)
    ax.set_ylabel("Δv (m/s)"); ax.set_ylim(0, 11800)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig2_waterfall.png")); plt.close(fig)
    print("fig2_waterfall.png")


# ------------------------------------------------------------------ fig 3
def fig3():
    rows = J("S1_bucket.json")
    fig, ax = plt.subplots(figsize=(9.5, 4.8))
    ax.set_title("Max-Q throttle bucket study (S1)")
    colors = {"no_bucket": GRAY, "35kPa": NAVY, "30kPa": ORANGE, "28kPa": RED}
    for row in rows:
        g = row["guidance"]; tag = row["q_limit"]
        qlim = {"no_bucket": None, "35kPa": 35e3, "30kPa": 30e3, "28kPa": 28e3}[tag]
        res = run_cfg(pitch_kick=math.radians(g["kick_deg"]), t_kick0=12, t_kick1=30,
                      s2_guidance="schedule", s2_bias0=math.radians(g["bias0_deg"]),
                      s2_bias_hold=g["hold_s"], jettison_fairing=True, q_limit=qlim)
        ts = [r[0] for r in res["rows"] if r[9] == "S1"]
        qs = [r[6] / 1000 for r in res["rows"] if r[9] == "S1"]
        ax.plot(ts, qs, color=colors[tag], lw=1.6,
                label=f"{tag}: Q={row['q_max_s1_kpa']:.1f} kPa, deficit {row['deficit_m_s']:.0f} m/s")
    ax.axhline(35, color=NAVY, ls=":", lw=1, label="structural limit 35 kPa")
    ax.scatter([60], [40.4], marker="s", color=RED, zorder=5, label="Day 5 own data point (40.4)")
    ax.set_xlabel("t (s)"); ax.set_ylabel("q (kPa)"); ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig3_bucket.png")); plt.close(fig)
    print("fig3_bucket.png")


# ------------------------------------------------------------------ fig 4
def fig4():
    rows = J("S2_split.json")
    fig, ax = plt.subplots(figsize=(9.5, 4.8))
    ax.set_title("Propellant-split boundary — single MVac locks the documented 391/112 split")
    xs = [r["p2_t"] for r in rows]
    ys = [r["deficit_m_s"] if r["deficit_m_s"] is not None else float("nan") for r in rows]
    feas = [r.get("feasible", False) for r in rows]
    tw = [r["s2_tw_ign"] for r in rows]
    ax.plot(xs, ys, "o-", color=NAVY, lw=1.6, label="deficit (surviving runs)")
    for x, y, f, t_ in zip(xs, ys, feas, tw):
        if not f:
            ax.scatter([x], [300], marker="x", color=RED, s=70, zorder=5)
            ax.annotate(f"crash\nT/W={t_:.2f}", (x, 300), textcoords="offset points",
                        xytext=(0, -32), ha="center", fontsize=8, color=RED)
    ax.axvspan(126, 140, color=RED, alpha=0.08)
    ax.text(133, 2600, "infeasible region:\nS2 arc sags (T/W≲0.62)", fontsize=9, color=RED, ha="center")
    ax.scatter([112], [2088], zorder=6, color=ORANGE, s=60)
    ax.annotate("documented split 391/112 (T/W=0.66)", (112, 2088), textcoords="offset points",
                xytext=(10, 120), fontsize=9,
                arrowprops=dict(arrowstyle="->", color=GRAY))
    ax.set_xlabel("S2 propellant (t)  [S1 prop = 503 t − S2, GLOM 600 t]")
    ax.set_xlim(110, 141)
    ax.set_ylabel("deficit to 500×500 (m/s)"); ax.set_ylim(0, 3400)
    ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig4_split_tw.png")); plt.close(fig)
    print("fig4_split_tw.png")


# ------------------------------------------------------------------ fig 5
def fig5():
    s3 = J("S3_payload.json"); s4 = J("S4_expendable.json"); s6c = J("S6c_exp2x_payload.json")
    fig, ax = plt.subplots(figsize=(9.5, 5.0))
    ax.set_title("Payload capability at 600 t GLOM — reusable vs expendable (vs 20 t requirement)")
    def series(rows, variant, color, style="o-", label=""):
        xs = [r["payload_t"] for r in rows if r.get("variant") == variant]
        ys = [r["deficit_m_s"] for r in rows if r.get("variant") == variant]
        if xs:
            ax.plot(xs, ys, style, color=color, lw=1.7, label=label)
    series(s3, "doc391", NAVY, label="reusable 1×MVac (as documented)")
    series(s3, "margin2prop", "#4C72B0", label="reusable 1×MVac (+margin→prop)")
    series(s4, "exp+m2p", ORANGE, label="expendable 1×MVac (+margin→prop)")
    xs = [r["payload_t"] for r in s6c]; ys = [r["deficit_m_s"] for r in s6c]
    ax.plot(xs, ys, "s-", color=RED, lw=1.7, label="expendable 2×MVac (+margin→prop)")
    ax.axhline(0, color=GREEN, lw=1.2)
    ax.axvline(20, color=GRAY, ls="--", lw=1)
    ax.text(20.1, 1800, "20 t requirement", rotation=90, fontsize=8, color=GRAY)
    ax.annotate("closes ≈ 6.5 t", (6.5, 0), xytext=(8.2, -650), fontsize=9, color="#4C72B0",
                arrowprops=dict(arrowstyle="->", color="#4C72B0"))
    ax.annotate("closes ≈ 14 t", (14, 0), xytext=(15.2, -650), fontsize=9, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED))
    ax.set_xlabel("payload (t)"); ax.set_ylabel("deficit to 500×500 (m/s)")
    ax.legend(fontsize=8, loc="upper left"); ax.set_ylim(-1200, 2600)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig5_payload.png")); plt.close(fig)
    print("fig5_payload.png")


# ------------------------------------------------------------------ fig 6
def fig6():
    opts = [
        ("Documented\n(1×MVac, 391/112)", 2088, GRAY),
        ("+ margin→S2 prop\n(§6.5 rule)", 1467, "#4C72B0"),
        ("+ 2nd MVac\n(T/W repair)", 872, NAVY),
        ("Expendable, 1×MVac\n(+reserve+HW→prop)", 1247, ORANGE),
        ("Expendable, 2×MVac", 542, "#C44E52"),
        ("S2-prop-only growth\n(2×/3× MVac)", None, RED),
        ("Scaled family\n12×M1D+4×MVac\nf≈1.39, GLOM≈802 t", -75, GREEN),
    ]
    fig, ax = plt.subplots(figsize=(10.5, 5.0))
    ax.set_title("Design-iteration ladder — 20 t to 500 km SSO deficit by option (600 t GLOM unless noted)")
    for i, (lab, val, col) in enumerate(opts):
        if val is None:
            ax.bar(i, 900, color="white", edgecolor=RED, hatch="///")
            ax.text(i, 950, "T/W barrier:\ninfeasible at any add", ha="center", fontsize=8, color=RED)
        else:
            ax.bar(i, val, color=col)
            ax.text(i, val + 60 if val > 0 else val + 120, f"{val:+,}", ha="center", fontsize=9)
    ax.text(6, 420, "closes at GLOM≈802 t\n(+34 %, re-scaled vehicle)", ha="center", fontsize=8, color=GREEN)
    ax.axhline(0, color="k", lw=0.8)
    ax.set_xticks(range(len(opts))); ax.set_xticklabels([o[0] for o in opts], fontsize=8)
    ax.set_ylabel("deficit to 500×500 SSO (m/s)"); ax.set_ylim(-500, 2600)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig6_ladder.png")); plt.close(fig)
    print("fig6_ladder.png")


if __name__ == "__main__":
    fig1(); fig2(); fig3(); fig4(); fig5(); fig6()
    print("all figures written to results/")
