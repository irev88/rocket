"""
plots2.py — Day 7 Arc B figures: fig7..fig13 into results/.
"""
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(__file__), "results")
J = lambda n: json.load(open(os.path.join(OUT, n)))

plt.rcParams.update({"font.size": 10, "axes.grid": True, "grid.alpha": 0.3,
                     "figure.dpi": 130})
NAVY, ORANGE, GREEN, RED, GRAY = "#16324F", "#E0561E", "#1E7A46", "#B3271E", "#6B7280"
PURPLE = "#6D28A8"


def fig7():   # recovery profile
    prof = J("R1_profile.json")
    t = np.array([r[0] for r in prof]); x = np.array([r[1] for r in prof]) / 1000
    h = np.array([r[2] for r in prof]) / 1000
    kind = [r[6] for r in prof]
    ship = J("R5_ship.json")["ship"]
    fig, ax = plt.subplots(figsize=(8.2, 4.2))
    for k, lab, c in (("ballistic", "ballistic coast", NAVY),
                      ("entry_burn", "entry burn (3 eng)", RED),
                      ("glide", "grid-fin glide (L/D taper)", GREEN)):
        m = np.array([kk == k for kk in kind])
        ax.plot(x[m], h[m], ".", ms=3, color=c, label=lab)
    ax.axvspan(ship["corridor_km"][0], ship["corridor_km"][1], color=ORANGE, alpha=0.15)
    ax.axvline(ship["x_ship_center_km"], color=ORANGE, ls="--",
               label=f"ship ~{ship['x_ship_center_km']} km")
    ax.annotate("SEP", xy=(x[0], h[0]), xytext=(x[0] - 40, h[0] + 18),
                arrowprops=dict(arrowstyle="->", color=GRAY))
    ax.set_xlabel("downrange x (km)"); ax.set_ylabel("altitude (km)")
    ax.set_title("fig7 — S1 recovery chain profile (documented SEP state, own model)")
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout(); fig.savefig(f"{OUT}/fig7_recovery_profile.png"); plt.close(fig)


def fig8():   # terminal ignition window
    r3 = J("R3_terminal_window.json")
    w = [r for r in r3["window"]]
    tl = [r["throttle"] for r in w]
    hign = [r["h_ign"] for r in w]
    prop = [r["burned"] / 1000 for r in w]
    ok = [r["v_final"] <= 2.2 for r in w]
    wc = [r for r in r3["window_conservative"]]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.2, 3.6))
    a1.plot([r["throttle"] for r in wc], [r["h_ign"] for r in wc], "s--", color=GRAY,
            label="conservative (kill |v|)")
    a1.plot([t for t, o in zip(tl, ok) if o], [h for h, o in zip(hign, ok) if o],
            "o-", color=NAVY, label="feasible (kill vh)")
    a1.plot([t for t, o in zip(tl, ok) if not o], [h for h, o in zip(hign, ok) if not o],
            "x", color=RED, ms=8, label="too slow to stop")
    a1.set_xlabel("throttle (1 engine)"); a1.set_ylabel("ignition altitude (m)")
    a1.legend(fontsize=8); a1.set_title("hover-slam ignition window (V-2)")
    a2.plot(tl, prop, "o-", color=GREEN)
    a2.axhspan(4.4, 6.3, color=ORANGE, alpha=0.12,
               label="deployed-family landing-burn anchor band")
    a2.set_xlabel("throttle (1 engine)"); a2.set_ylabel("landing propellant (t)")
    a2.legend(fontsize=8); a2.set_title("landing prop vs throttle")
    fig.suptitle("fig8 — terminal descent: 176–217 m/s requirement vs Day-6 '≈100 m/s' quota")
    fig.tight_layout(); fig.savefig(f"{OUT}/fig8_terminal_window.png"); plt.close(fig)


def fig9():   # reserve closure
    r4 = J("R4_closure.json")
    cor = [("M2.7", r4["corridors"]["M2.7"]), ("M2.3", r4["corridors"]["M2.3"]),
           ("M2.0", r4["corridors"]["M2.0"]), ("M1.8", r4["corridors"]["M1.8"])]
    fig, ax = plt.subplots(figsize=(7.6, 3.8))
    y = np.arange(len(cor))
    for i, (k, v) in enumerate(cor):
        if v.get("R_star_t") is None:
            continue
        ax.barh(i, v["entry_t"], color=NAVY, label="entry burn" if i == 0 else None)
        ax.barh(i, v["landing_t"], left=v["entry_t"], color=GREEN,
                label="landing" if i == 0 else None)
        ax.barh(i, v["aux_t"], left=v["entry_t"] + v["landing_t"], color=GRAY,
                label="aux (RCS+margin)" if i == 0 else None)
        ax.text(v["R_star_t"] + 0.4, i, f"R*={v['R_star_t']:.0f} t", va="center", fontsize=9)
    ax.axvline(r4["documented_reserve_t"], color=RED, lw=2, ls="--",
               label=f"documented {r4['documented_reserve_t']:.0f} t")
    ax.axvline(r4["documented_legged_t"], color=ORANGE, lw=1.5, ls=":",
               label=f"Day-4 legged {r4['documented_legged_t']:.0f} t")
    ax.set_yticks(y, [c[0] for c in cor]); ax.set_xlabel("recovery reserve (t)")
    ax.set_xlim(0, 46)
    ax.legend(fontsize=8, loc="lower right")
    ax.set_title("fig9 — recovery reserve closure R* by entry corridor (own model)")
    fig.tight_layout(); fig.savefig(f"{OUT}/fig9_reserve_closure.png"); plt.close(fig)


def fig10():  # LHS Spearman drivers
    s8 = J("S8_sensitivity.json")
    facs = ["t_kick0", "p1", "kick", "bias0", "hold", "cd"]
    labels = ["t_kick0 (s)", "S1 prop (t)", "kick (deg)", "loft bias0 (deg)",
              "bias hold (s)", "Cd scale"]
    fig, ax = plt.subplots(figsize=(7.6, 3.8))
    y = np.arange(len(facs)); wdt = 0.38
    for j, (nm, c) in enumerate((("A", NAVY), ("B", ORANGE))):
        rho = [s8[nm]["spearman"]["deficit"][f]["rho"] for f in facs]
        ax.barh(y + (j - 0.5) * wdt, rho, height=wdt, color=c,
                label=f"config {nm}")
    ax.axvline(0, color="k", lw=0.8)
    ax.set_yticks(y, labels); ax.set_xlabel("Spearman ρ vs deficit to 500×500 (converged runs)")
    ax.legend(fontsize=9)
    ax.set_title("fig10 — B2 LHS sensitivity: deficit drivers (600 samples/config)")
    fig.tight_layout(); fig.savefig(f"{OUT}/fig10_lhs_drivers.png"); plt.close(fig)


def fig11():  # DE convergence
    s9 = J("S9_optimized.json")
    fig, ax = plt.subplots(figsize=(7.4, 3.8))
    for nm, c, grid in (("A", NAVY, 1467), ("B", ORANGE, 872)):
        h = s9[nm]["history"]
        ax.plot([e for e, _ in h], [v for _, v in h], "-", color=c,
                label=f"config {nm} best-so-far")
        ax.axhline(grid, color=c, ls=":", alpha=0.6, label=f"config {nm} grid-tuned ({grid})")
    ax.set_xlabel("function evaluations"); ax.set_ylabel("penalised deficit (m/s)")
    ax.set_ylim(700, 1800)
    ax.legend(fontsize=8)
    ax.set_title("fig11 — B3 differential-evolution convergence (guidance family ceiling)")
    fig.tight_layout(); fig.savefig(f"{OUT}/fig11_de_convergence.png"); plt.close(fig)


def fig12():  # ascent MC
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.8))
    for ax, nm, c in ((axes[0], "A", NAVY), (axes[1], "B", ORANGE)):
        rows = J(f"S10_samples_{nm}.json")
        conv = np.array([r["deficit"] for r in rows if r["converged"]])
        safe = np.array([r["deficit"] for r in rows if r["converged"] and r["q_kpa"] <= 35.0])
        ax.hist(np.clip(conv, 0, 6500), bins=40, color=c, alpha=0.45,
                label=f"all converged (n={len(conv)})")
        ax.hist(np.clip(safe, 0, 6500), bins=40, color=c, alpha=0.9,
                label=f"q≤35 kPa only (n={len(safe)})")
        s10 = J("S10_mc_ascent.json")[nm]["conditioned"]
        ax.set_title(f"config {nm}: P(conv)={s10['P_converge']:.2f}, "
                     f"P(survive q)={s10['P_struct_survival_qle35']:.2f}, "
                     f"P(q&g)={s10['P_survive_q_and_g']:.2f}", fontsize=9)
        ax.set_xlabel("deficit to 500×500 (m/s)"); ax.legend(fontsize=8)
    fig.suptitle("fig12 — B5 ascent Monte-Carlo (400/config): fragility at the T/W cliff")
    fig.tight_layout(); fig.savefig(f"{OUT}/fig12_mc_ascent.png"); plt.close(fig)


def fig13():  # recovery MC
    s11 = J("S11_mc_recovery.json")
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.2, 3.6))
    for nm, c in (("P0_documented", GRAY), ("P1_sized_M23", GREEN)):
        rows = [r for r in J(f"S11_samples_{nm}.json") if r["ok"]]
        x = [r["x_km"] for r in rows]
        a1.hist(x, bins=30, alpha=0.55, color=c,
                label=f"{nm} (n={len(rows)})")
        need = [r["total_t"] for r in rows]
        a2.hist(need, bins=30, alpha=0.55, color=c,
                label=f"{nm}: reserve {s11[nm]['reserve_t']} t")
        a2.axvline(s11[nm]["reserve_t"], color=c, ls="--")
    a1.set_xlabel("capture downrange x (km)"); a1.set_title("capture corridor spread")
    a2.set_xlabel("total reserve need (t)"); a2.set_title("reserve need vs plan")
    a1.legend(fontsize=8); a2.legend(fontsize=8)
    fig.suptitle("fig13 — B5 recovery Monte-Carlo (500/plan): P0 closes P=0.0, P1 sized P=0.45")
    fig.tight_layout(); fig.savefig(f"{OUT}/fig13_mc_recovery.png"); plt.close(fig)


if __name__ == "__main__":
    for f in (fig7, fig8, fig9, fig10, fig11, fig12, fig13):
        f(); print(" ", f.__name__, "ok")
