# Day 7 — Repaired Simulation: Key Results Data Sheet

**Date**: 2026-07-17 (Day 7) · **Model**: `day7_sim/` rebuilt 3-DOF planar ascent simulator (RK4, spherical Earth, USSA76, honest Isp(h))
**Validation**: `validate.py` gate **8/8 PASS** (`results/gate.json`) — Isp in-envelope, mass bookkeeping exact, energy balance residual 3 m/s, real-flight band sanity
**Everything below is reproducible**: `python3 studies.py && python3 validate.py && python3 plots.py`

---

## 1. Headline numbers (use in Day 7 report)

| # | Quantity | Value | Context / method |
|---|---|---|---|
| H-1 | **Δv deficit of the documented design** to 500×500 SSO, 20 t payload | **2,088 m/s** | honest sim at documented 600 t / 391/112 split / 1× MVac; Hohmann-accounting from SECO apsides |
| H-2 | Old master-data implied effective Isp | S1 ≈ **364 s** (envelope 282–311); S2 ≈ **427 s** (declared 348) | (old v-gain + honest losses)/(g0·ln ratio) → **C-1 phantom energy re-derived** |
| H-3 | Honest Max-Q | **31.2 kPa @ t+70 s / 11.0 km / Mach 1.41** | vs Day 5 claim 28 kPa @ 12–15 km vs Day 5 own data 40.4 kPa @ 9.3 km → **claim contradicted by own data** |
| H-4 | Honest staging (V-1) | **t+142 s, 66.5 km, 1,892 m/s, γ=40.7°, Mach 5.7, downrange 51 km, mass 209 t** | vs Day 5 claim 78 km / 2,520 m/s / Mach 8.2 |
| H-5 | Final state | SECO t+535 s, 78 km*, 5,939 m/s, γ=−17° → perigee −3,823 km | *arc sag — guidance-family artifact, see limitations |
| H-6 | Honest ideal Δv (Tsiolkovsky) | S1 3,135 + S2 4,740 = **7,875 m/s** vs recorded requirement 11,000 | requirement itself ≈ +1,100–1,400 m/s padded vs physical need (7,612 orbital + ~1,900 losses) |
| H-7 | Ascent loss decomposition | gravity 1,810 (S1 1,217 + S2 593) / drag 18–26 / steering 82–108 m/s | energy balance residual 3 m/s (G7) |
| H-8 | **Reusable payload capability at 600 t** | **≈ 6.6 t** (with margin→prop); **< 2.5 t** (as documented) | sim closure points (S7) |
| H-9 | Expendable payload at 600 t (1× MVac, +margin→prop) | **≈ 7.3 t** | removes 5.5 t recovery HW, burns 18 t reserve |
| H-10 | +2nd MVac (T/W repair, +0.55 t dry) at 600 t, 20 t | deficit 1,557 → **872 m/s** w/ margin→prop | S2 T/W at ignition 0.66 → 1.32 |
| H-11 | Expendable + 2× MVac at 600 t | closes at **≈ 14 t** payload | 20 t still 542 m/s short |
| H-12 | **Only verified 20 t-to-SSO closure** | **scaled family: 12× M1D + 4× MVac, prop ×1.39 ⇒ GLOM ≈ 802 t (+34 %)** | sim points f=1.40 (−75) & f=1.45 (−220, braking margin); interpolated f≈1.39 |
| H-13 | T/W barrier | S2-prop-only growth infeasible: crash boundary at **S2 T/W_ign ≈ 0.62–0.66**; GLOM-only growth needs S1 thrust (liftoff T/W → ~1.05 at 750 t) | S5 / S6b probes |

## 2. Iteration ladder (20 t to 500 km SSO, deficit m/s)

| Option | Deficit | ΔGLOM | Verdict |
|---|---:|---:|---|
| L0 Documented (1× MVac, 391/112, margin as dry) | +2,088 | — | infeasible as documented |
| L1 + 7 t margin → S2 prop (Day 4 §6.5 rule) | +1,467 | 0 | free win, −621 m/s |
| L2 + 2nd MVac (T/W repair) | +872 (L1 included) | +0.55 t dry | best 600 t point; reusable capability ≈ 12 t |
| L3a Expendable 1× MVac (+reserve & HW → prop) | +1,247 | −5.5 t | worse than L2 (prop in S1 is low-Isp) |
| L3b Expendable 2× MVac | +542 | −5.5 t +0.55 t | closes at 14 t payload |
| L4 S2-prop-only growth (1×/2×/3× MVac) | ✗ T/W barrier | — | infeasible: S2 arc sags / S1 T/W < 1.1 |
| L5 **Scaled family (12× M1D + 4× MVac, f ≈ 1.39)** | **−75 (verified)** | **≈ 802 t (+34 %)** | only architecture-level closure keeping 20 t + reuse |

## 3. Trajectory/guidance corrections implemented (model repair log)

| Fix | Before (Day 5) | After (Day 7) |
|---|---|---|
| F-a | Isp effectively constant ~296 s (S1) / inflated post-facto (S2 net > ideal) | Isp(h) = 282 + 29·(1 − p/p0), hard ceiling at vacuum value; S2 constant 348 |
| F-b | S2 prograde "guidance" (implicit) produced phantom Δv | explicit PEG-like loft-bias schedule + end-game attitude floor (θ ≥ −1.5°); steering loss measured (82–192 m/s) |
| F-c | Max-Q claimed 28 kPa, unmeasured | q(t) recorded every step; bucket controller implemented & costed (28 kPa cap ⇒ +21 m/s deficit, MECO −3.2 km) |
| F-d | No axial-g check | sensed accel tracked: max 4.09 g (< 5 g limit, no throttle-down required) |
| F-e | fairing carried to orbit (39 t final) | fairing jettisoned at q < 100 Pa after S2 ignition (final 37.2 t) — worth ~+100 m/s |
| F-f | trajectory ended suborbital, unflagged | orbit elements + Hohmann deficit computed every run |

## 4. New V-1 data for Day 6 recovery chapter

| Config | MECO (t, h, v, γ, Mach, downrange) | Note |
|---|---|---|
| Documented (honest) | 142 s, 66.5 km, 1,892 m/s, 40.7°, 5.7, 51 km | v 18 % below Day-6 anchor 2.0–2.3 km/s — **recovery Δv quota check needed** |
| 2× MVac tuned (kick 5.5°) | 142 s, 51.4 km, 2,043 m/s, 21.3°, 6.2, ~79 km | flatter corridor, closer to Day-6 anchor; downrange catch geometry friendlier |
| Expendable 1× MVac | 149 s, ~109 km?, 2,237 m/s | hotter staging (no recovery reserve burn) |

*Implication for Day 6: entry-burn/terminal quotas (500–800 + 200–300 m/s) were sized for v_sep ≈ 2.0–2.3 km/s; honest 1.89 km/s (baseline) or 2.04 km/s (L2) are inside/beside that band — flag as Day 7→8 consistency item, re-run Day-6 closure with the chosen architecture point.*

## 5. Limitations & honesty flags (state in report)

1. **Guidance is a tuned family, not an optimizer**: per-point best of a small grid (kick angle × loft-bias schedule). Deficits are *upper bounds* — a real collocation/PEG optimizer (B3) may shave ~100–300 m/s. Conclusions (multi-hundred-to-2,000 m/s gaps) are unaffected.
2. **End-game arc sag**: 1× MVac configs dip to ~45–80 km late-burn (SECO γ ≈ −15°); energetically accounted, operationally undesirable — real guidance would hold altitude better (slightly more steering loss).
3. Deficit uses **impulsive Hohmann accounting** from SECO apsides; negative deficit = arrival at target circle with excess speed (braking margin, requires S2 restart — Day 3 capability ✓).
4. **No Earth-rotation credit** (conservative for SSO retrograde ~97.4°; plane-change none).
5. Cd(Mach) is an engineering correlation; aero-thermal/entry heating not modeled; wind/dispersions not yet (Monte-Carlo = B5).
6. Scaled-family (L5) dry-mass scaled as 40 t→50.3 t (n^0.8 heuristic) — rough.
7. Documented engine inconsistency (CR-D7-01): Merlin SL 845 kN + Isp 282/311 ⇒ vac thrust 932 kN vs documented 914 kN (+1.9 %); mdot calibrated to SL point.

## 6. File map

```
day7_sim/
├── params.py        # all documented constants + traceability
├── atmosphere.py    # USSA76 exponential layers (validated vs standard)
├── vehicle.py       # Isp(h), thrust, Cd(Mach) — honesty rules
├── sim.py           # 3-DOF RK4 simulator + per-point guidance
├── studies.py       # S0–S6+S7 suites → results/*.json
├── validate.py      # 8-gate audit gate → results/gate.json (8/8 PASS)
├── plots.py         # fig1–fig6 → results/fig*.png
├── tune_kick.py     # (superseded) early kick tuner
├── results/         # JSON + PNG, all citable
└── DATA_SHEET.md    # this file
```

---

## 7. Arc B additions (evening session) — DOE, optimization, Monte-Carlo, recovery chain

Reproduce: `python3 run_recovery.py && python3 doe.py && python3 mc.py && python3 plots2.py`

### 7.1 Headline numbers (B-arc)

| # | Quantity | Value | Context / method |
|---|---|---|---|
| H-14 | **Recovery reserve fixed point R\*** (entry+landing+aux closure) | **30–37 t** by corridor: M2.7→29.6 t, M2.3→32.4 t, M2.0→35.0 t, M1.8→37.2 t | grid-scan fixed point `need(R) ≤ R`, entry sized per mass (R4); aux = 2 t own estimate |
| H-15 | Deepest entry corridor at **documented 18 t** reserve | **Mach 2.89** at 40 km (17.9 t, tl 0.67) — anchored reusable-family corridor is Mach 1.8–2.7 | R2 throttle scan with dry-mass floor; quota 500–800 m/s only reaches Mach ≈4.3 |
| H-16 | Terminal ignition window (V-2) | ignite **≈1,500–2,000 m**, burn **12–21 s**, landing prop **4.6–4.8 t** (1 eng, adaptive) | R3 bisection per throttle; conservative kill-|v| variant 4.64 t; bracket consistent with deployed-family anchors 4.4–6.3 t |
| H-17 | **Ship capture position (V-4 preliminary)** | **489 km** downrange centre; corridor 481–496 km (L/D ±20 %); MC spread 474–490 km (p5–p95) | R5 L/D sweep + S11 Monte-Carlo; vs Day-6 “300–600 km” band ⇒ inside, OK |
| H-18 | B2 LHS drivers of ascent deficit | t_kick0 (+0.48/+0.54), S1 prop (−0.42/−0.45), kick (−0.41/−0.43), loft bias (+0.22/+0.43) | 600 samples/config; Spearman on converged; hold & Cd weak (\|ρ\| ≤ 0.13) |
| H-19 | B3 guidance-family ceiling (differential evolution) | A (1×MVac+m2p): **1,427 m/s** (grid 1,467, gain −40); B (2×MVac+m2p): **871 m/s** (grid 872, gain −1) | the Arc-A grid was already at the guidance-family ceiling ⇒ H-deficits are **tight upper bounds**, not loose |
| H-20 | **B3 constraint finding** | config B optimum has g_max **6.2 g** (limit 5 g); g-constrained DE still converges to 6.2 g | axial-g exceedance is **structural** (2×981 kN vs ~40 t burnout mass), not tunable by guidance → CR-D7-07 |
| H-21 | B5 ascent MC (400/config, 2σ dispersions) | A: P(converge)=0.82, P(q≤35)=0.45, deficit given safe = 1,496±54 m/s; B: P(converge)=0.94, P(q≤35)=0.38, **P(q≤35 ∧ g≤5)=0.00**, deficit given safe = 928±51 | open-loop schedule at T/W 0.66 cliff: Isp −1.5 s (2σ) alone ⇒ +4,600 m/s or dive → knife-edge confirmed by construction |
| H-22 | B5 recovery MC (500/plan) | documented 18 t plan: **P(close within reserve)=0.00** (p95 need 24.6 t); sized M2.3 plan at R\*=32.4 t: P=**0.45** (p95 need 34.3 t ⇒ size at **≈34.5–36 t**) | CD_A U(12–32), L/D ±20 %, throttle ±2.5 %, adaptive landing retarget |

### 7.2 Iteration log updates (Arc C)

* **Iteration 2 (recovery reserve)**: documented 18 t → model closure **R\* ≈ 30–37 t** by corridor (recommended Day-8 sized point **≈34.5 t**, M2.3 corridor, MC-p95). Day-4's legged-fallback 24 t also undersized; **Day-6 hybrid saving claim (−2.5 t HW −6 t reserve) unsupported** — reserve need is ≥ legged case; the 2.5 t HW saving stands but is second-order.
* **Iteration 3 (loads/corridor + robustness)**: (i) Day-6 terminal quota “≈100 m/s” → model **176–217 m/s at 2 km** ⇒ landing prop 4.6–4.8 t (now budgeted); (ii) 2×MVac config exceeds 5 g at SECO structurally (6.2–6.4 g) → options: S2 throttle authority, 6 g cargo limit, or accept deficit; (iii) ascent optima are knife-edge at T/W≈0.66 ⇒ Day-8 architecture decision must carry robustness margin, not just nominal deficit.

### 7.3 Additional limitations (state in Day 9–10 report)

8. Recovery chain gravity uses a spherical-central approximation without centrifugal terms (2-DOF downrange frame); ballistic arc cross-checked vs energy conservation, entry-state consistent at ~3 % level; capture-x accuracy order ±10 km.
9. Terminal phase: grid fins assumed to verticalise (L/D taper 10→2 km); residual horizontal ~85 m/s at 2 km is nulled by assumption (gimbal/aero flare not modeled); hover-slam is 1-D vertical.
10. Ascent MC dispersions applied to *open-loop* tuned guidance (no closed-loop correction) → survival probabilities are pessimistic \*for a real closed-loop vehicle\* but honestly represent our guidance family.
11. DE optimization explored the schedule guidance family only; true free-form collocation could still differ (flagged follow-on, not blocking).
