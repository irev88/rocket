# Day 7 — AI-Assisted Trajectory Optimization, Sensitivity & Monte-Carlo: Working Notes

**Date**: 2026-07-17 (Day 7 of 10) · **Status**: *working notes — not a finalized report or presentation.*
**Scope completed**: Arc A (physics repair & validation of the ascent baseline), B2 (DOE/sensitivity), B3 (trajectory optimization), B4 (recovery sub-problem), B5 (Monte-Carlo robustness), Arc C (design-iteration log).
**Reproducibility**: every number below regenerates from `day7_sim/` (`studies.py`, `validate.py`, `run_recovery.py`, `doe.py`, `mc.py`, `plots.py`, `plots2.py`); machine-readable detail in `day7_sim/DATA_SHEET.md` and `day7_sim/results/*.json`.

---

## 1. What was done today

| Arc | Task | Status | Key artifacts |
|---|---|---|---|
| A | Repair & validate the physics baseline (audit counter-measures) | **Done** — 8/8 audit gates PASS | `day7_sim/`, `results/gate.json`, figs 1–6, `05_Day5_Repair_and_Completion.md` |
| B1 | (folded into A) honest staging point for recovery work | Done | `S0_baseline.json` |
| B2 | Design of experiments / sensitivity of the trajectory | **Done** — 1,200 LHS runs | `S8_*.json`, fig10 |
| B3 | Trajectory optimization | **Done** — differential evolution, ~3,500 evals + g-constrained rerun | `S9_optimized.json`, fig11 |
| B4 | Recovery sub-problem | **Done** — full chain model + closure | `R1–R5 json`, figs 7–9 |
| B5 | Monte-Carlo robustness | **Done** — 800 ascent + 1,000 recovery samples | `S10/S11 json`, figs 12–13 |
| C | Design-iteration log | **Done** — Iterations 1–3 documented | §5 below, `DATA_SHEET.md` §7.2 |

---

## 2. Methods (what is ours, what is anchored)

**Own models only for inputs** — all vehicle/mission inputs come from our own Day 1–4 documented parameters or our own model outputs (uniqueness rule). External rocket data appear **only as validation anchors**, itemized in §3 and never used as model inputs.

1. **Ascent simulator** (Arc A, rebuilt): 3-DOF planar over spherical Earth, RK4 fixed step, USSA76 exponential atmosphere, honesty rules: Isp(h) pressure-interpolated and hard-ceilinged at vacuum value; vacuum stage at constant vacuum Isp; event-driven phases with Max-Q bucket controller and axial-g governor; per-step loss decomposition (thrust/gravity/drag/steering integrals); orbit apsides + Hohmann deficit at SECO. Validation: 8/8 gates (Isp in envelope, mass bookkeeping exact to 0.1 kg, energy-balance residual 3 m/s, atmosphere vs standard tables, real-flight band sanity).
2. **Recovery chain simulator** (B4): 2-DOF RK4 chain — ballistic coast → 3-engine retrograde entry burn (altitude-targeted corridor) → unpowered atmosphere descent with grid-fin pseudo-lift (L/D, tapered to zero between 10 and 2 km so the endgame verticalises, mirroring deployed-family practice) → 1-D vertical hover-slam with per-throttle ignition-altitude bisection → capture interface at 15 m / ≤2 m/s. Burns are **reserve-limited** (dry-mass floor) — an early-session bug let the entry burn consume structure ("m = 17 kg" artifact); found and fixed, results rerun (this is why R4 numbers supersede the morning guesses).
3. **DOE** (B2): Latin hypercube, 600 samples per leading config over 6 factors (kick 2.5–6°, t_kick0 10–20 s, loft bias 0–28°, bias hold 160–360 s, S1 prop 350–391 t, Cd scale 0.8–1.2); Spearman rank correlations on converged runs; crash = infeasible marker, mapped by factor tertile.
4. **Optimization** (B3): scipy `differential_evolution` on the 4 guidance DOF per config, deficits penalized for q > 35 kPa, MECO < 50 km, g > 5; polishing on; seeds fixed. A second run with a hard g-penalty tested whether guidance alone can make config B satisfy the 5 g limit.
5. **Monte-Carlo** (B5): ascent — 400 samples/config, Normal dispersions (2σ: Isp ±1.5 s, Cd ±10%, dry masses ±1%, kick ±0.15°, t_kick0 ±1 s). Recovery — 500 samples/plan, CD_A ~ U(12–32 m²), L/D ±20%, entry-throttle execution ±2.5% (2σ), adaptive (re-targeted) landing ignition per sample.
6. **Configurations carried through B2–B5** (the leading Day-8 candidates at 600 t / 20 t payload):
   * **Config A "L1"**: 1× MVac, margin→propellant (S2 119 t); grid deficit 1,467 m/s.
   * **Config B "L2"**: 2× MVac (+0.55 t dry), margin→propellant; grid deficit 872 m/s.

---

## 3. Findings

### 3.1 Ascent baseline & design space (Arc A + B2 + B3)

* **The documented design does not close**: honest deficit **2,088 m/s** to 500×500 SSO at 20 t payload (600 t GLOM, 391/112 split, 1× MVac). The old trajectory table's implied Isp (S1 ≈ 364 s, S2 ≈ 427 s — both above their own vacuum values) is the energy non-conservation found in the audit (C-1 re-derived quantitatively).
* Honest anchors for downstream work: MECO t+142 s / 66.5 km / 1,892 m/s / γ 40.7° / Mach 5.7 / 51 km downrange; Max-Q 31.2 kPa @ 11.0 km / Mach 1.41 (Day-5 claim of 28 kPa is contradicted by Day-5's own data, 40.4 kPa — both logged in the CR register).
* **Iteration ladder** (deficit at 20 t, reusable unless stated): documented +2,088 → margin→prop +1,467 → +2nd MVac +872 → expendable-2× +542 (closes at ≈14 t) → S2-prop-only growth hits the **T/W barrier** (crash boundary S2 T/W ≈ 0.62–0.66) → **only architecture-level closure: scaled family 12× M1D + 4× MVac at ≈802 t GLOM (prop ×1.39)**. Reusable payload at 600 t: ≈6.6 t.
* **Sensitivity (B2)**: deficit is controlled by guidance-timing factors (t_kick0 ρ≈+0.5, kick ρ≈−0.42, loft bias ρ≈+0.2…+0.4) and S1 prop (ρ≈−0.43); Cd is a weak deficit factor (|ρ|≤0.05) though it controls drag *loads*. Config A crashes in 9% of LHS space (corners: high kick, early kick, low S1 prop); config B is feasible everywhere (T/W robustness).
* **Optimization (B3)**: the Arc-A hand-tuned grid points were already at the guidance-family ceiling — DE buys only **40 m/s for A (1,427)** and is **equal for B (871)**. Honest consequence: reported deficits are **tight** upper bounds; more exotic guidance will not rescue 600 t / 20 t.
* **New structural finding (CR-D7-07)**: config B ends the S2 burn at **6.2–6.4 g** vs the 5 g limit at *every* guidance tried, including a g-penalized DE rerun — the exceedance is in the thrust-to-burnout-mass ratio, not the trajectory. Options for Day 8: (i) give S2 throttle authority, (ii) raise the cargo limit to 6 g, (iii) accept a higher-deficit point. **This changes the L2 ranking story and must be in the Day-8 trade.**

### 3.2 Recovery sub-problem (B4)

Chain driven entirely by our own SEP state (66.5 km, 1,892 m/s, γ 40.7°):

* Ballistic arc: 258 s, entry interface at 70 km at 1,806 m/s / γ ≈ −42°, apogee ≈143 km.
* **Entry corridor sizing vs reserve (R2/R4)**:
  * At the **documented 18 t reserve** the deepest reachable corridor is **Mach 2.89 at 40 km** (tl 0.67, 17.9 t) — i.e., Day 2/6's entry quota (500–800 m/s) buys only a Mach ≈4+ corridor and is **not** a credible reuse corridor.
  * Fixed-point closure R\* = entry(R) + landing(R) + aux(2 t): **M1.8 → 37.2 t, M2.0 → 35.0 t, M2.3 → 32.4 t, M2.7 → 29.6 t**. The Day-4 reserve (18 t) is undersized ≈2×; the Day-4 *legged* fallback number (24 t) is also undersized ⇒ **Day-6's claimed hybrid saving (−2.5 t HW *and* −6 t reserve) is not supported**: the 2.5 t hardware saving stands, the 6 t reserve saving does not.
* **Terminal descent (V-2)**: glide exit ≈ 176–217 m/s at 2,015 m (verticalising under fin taper). Hover-slam ignition ≈ 1,500–2,000 m, 12–21 s burn, **landing propellant 4.6–4.8 t** (adaptive throttle). Day-6's "≈100 m/s terminal quota" is superseded — iteration-3 item.
* **Ship position (V-4 preliminary)**: capture at **489 km** downrange centre, L/D-uncertainty corridor 481–496 km, MC p5–p95 474–490 km → inside Day-6's 300–600 km band. Ship placement is a *consequence* of the Day-8 architecture choice (SEP state moves with MECO), so this is preliminary.

### 3.3 Robustness (B5)

* **Ascent MC is the sharpest Day-7 finding.** At the DE-optimal open-loop guidance:
  * Config A: P(reach SECO) = 0.82, P(structural survival q≤35 kPa) = **0.45**; survivors tightly clustered (deficit 1,496 ± 54 m/s). Failure mode is not scatter — it is **dive/break-up at the T/W = 0.66 cliff** (a 2σ Isp shortfall alone costs +4,600 m/s or the trajectory).
  * Config B: P(SECO) = 0.94, P(q≤35) = 0.38, **P(q≤35 ∧ g≤5) = 0.00** — the g-exceedance is 100% robust (CR-D7-07 confirmed statistically).
  * Interpretation: our guidance family is open-loop; a closed-loop (PEG-class) vehicle would recover part of the lost robustness, but the *knife-edge at T/W ≈ 0.66 is real* (matches the L4 crash boundary). Day-8's architecture decision must carry a robustness margin, not just nominal deficits.
* **Recovery MC**: documented-reserve plan **P(close within 18 t) = 0.00** (p95 need 24.6 t, and 41% of samples even exhaust reserve mid-entry). The M2.3 corridor sized at R\* = 32.4 t closes with P = 0.45 (adaptive landing); **size at ≈ 34.5–36 t (MC p95)** or add L/D/entry-load margin — input to Day 8.

### 3.4 Verification against external anchors (validation only — not inputs)

| Our model output | External anchor (validation only) | Match? |
|---|---|---|
| Entry burn 70→40 km, 3 engines, exit Mach 1.8–2.7 corridor | Deployed-family infographics: entry burn ~70→40 km [zlsadesign.com F9 DPL]; NASA-observed reentry burns 70–40 km [en.wikipedia.org/wiki/Falcon_9_first-stage_landing_tests] | ✓ corridor geometry anchored |
| Entry burn prop 22–30 t at credible corridors (Δv ≈ 1,150–1,450 m/s at 58–78 t stack) | GTO-class estimate ≈21 t / ≈1,690 m/s at ~3×full throttle [r/SpaceXLounge SES-10 analysis] | ✓ magnitude class (theirs hotter: higher sep energy) |
| Landing prop 4.6–4.8 t, ignition ~1.5–2 km, TWR at ignition ≈1.8 | ≈4.4–6.3 t, Δv ≈490–690 m/s, TWR ≈1.7, burn ≈29–32 s [r/spacex hover-slam analysis; orbitalxploration.com Block 5 summary] | ✓ band overlap |
| Grid fins hold to low altitude, vertical endgame | fins deploy/steer from ~70 km, single-engine landing <2 m/s touchdown [orbitalxploration.com; zlsadesign] | ✓ qualitative practice mirrored in taper assumption |
| Empty-ish booster recovery is *the* cost driver (relevance of reserve mass) | booster = 60–75% of vehicle cost; reflights 157/165 in 2025 [TechTimes S-1 economics] | ✓ motivation, not a model input |

No external performance number was imported as a model input; divergences from anchors are explainable (our sep energy is lower → corridor targets slightly gentler at equal mass).

### 3.5 Consistency vs previous project results

* Matches: Day-4 mass budget arithmetic (closes exactly); Day-2 staging-altitude class; Day-6 ship band; Day-6 entry-burn geometry (70→40 km).
* Superseded (all logged): Day-5 trajectory table (retired, 5 defects), Day-5 Max-Q claim, Day-6 Δv quotas (entry 500–800 / terminal ~100 m/s), Day-6 hybrid reserve-saving claim (−6 t), V-1 staging point, Day-2 "11.0 km/s required" (padded +1,100–1,400 vs Hohmann need — CR-D7-02).
* CR register additions today: **CR-D7-06** (Day-6 recovery-reserve/quotas under-scoped ~2×; reserve saving unsupported → Day-6 doc addendum pending Day-8), **CR-D7-07** (2×MVac structural 6.2–6.4 g > 5 g limit at all guidance points → Day-8 decision item).

---

## 4. Design-iteration log (Arc C)

**Iteration 1 — performance repair (600 t, reusable)**: documented +2,088 → margin→prop +1,467 → 2×MVac +872 m/s; reusable 20 t remains infeasible at 600 t ⇒ candidates for Day 8: (a) 600 t reusable ≈ 6.6–12 t payload class, (b) 600 t expendable 20 t fails by 542 m/s (closes at 14 t), (c) **rescued requirement: ≈802 t scaled family (verified −75 m/s at f=1.40)**.

**Iteration 2 — recovery reserve**: 18 t documented → model closure **R\* 30–37 t** by corridor; recommend Day-8 working point **M2.3 corridor, ≈34.5 t** (MC p95-informed). Entry hardware unchanged; the *propellant* book grows, not the structure — GLOM-neutral if traded against the L4-style prop growth once architecture is chosen.

**Iteration 3 — loads, corridor & robustness**: (i) terminal-descent reality (176–217 m/s at 2 km) replaces the ≈100 m/s quota; landing burn ≈4.6–4.8 t budget; (ii) config B axial-g exceedance (structural) logged as CR-D7-07 with three resolution paths; (iii) ascent optima are knife-edge (P_survival 0.38–0.45 open-loop) → Day-8 decision scoring must include a robustness criterion and a closed-loop guidance assumption; (iv) ships at ≈490 km nominal.

---

## 5. Verification status of Day-6 targets

| Target | Status | Note |
|---|---|---|
| V-1 honest staging point | **Closed** | 66.5 km / 1,892 m/s / γ 40.7° / 51 km downrange (Day-6 deck v1.1 already flagged) |
| V-2 terminal ignition window | **Closed** | h_ign ≈ 1,500–2,000 m, 1 eng tl 0.75–1.0, 4.6–4.8 t prop |
| V-3 catch interface loads | **Open → Day 8/9** | capture at ≤2 m/s modeled; net/cable dynamics out of scope for reduced-order chain |
| V-4 ship position & corridor | **Preliminary closed** | 489 km centre, 15–20 km corridor; re-solve after Day-8 architecture pick |

---

## 6. Open items for Day 8 (reliability & economics)

1. **Architecture decision** (CR-D7-04) with today's inputs: A ~6.6 t reusable / B 12 t reusable (but CR-D7-07 g-fix needed) / expendable-2× 14 t / 802 t rescale @ 20 t reusable — plus recovery reserve ≈34.5 t in all reusable cases (GLOM trade).
2. Choose g-limit path (S2 throttle vs 6 g cargo limit vs deficit acceptance).
3. Fold recovery reserve into reliability/availability math (booster cost fraction anchor 60–75%); turnaround/refurb anchors collected for economics model.
4. Closed-loop guidance assumption memo (how much MC survival to credit to PEG-class guidance vs our open-loop family) — needed before quoting mission reliability.
5. Re-solve V-4 ship position at the chosen architecture's SEP state.

## 7. Limitations carried (state in final report)

Reduced-order models (3-DOF ascent, 2-DOF recovery, 1-D terminal); no Earth-rotation credit; engineering Cd(Mach) and pseudo-lift glide; spherical-gravity recovery frame (≈3 % energy-consistent, ±10 km capture-x class); DE inside the schedule guidance family only; ascent MC uses open-loop guidance (survival probabilities pessimistic); external anchors used for validation only; aux recovery allowance (2 t) is an own estimate. Full list: `day7_sim/DATA_SHEET.md` §5 & §7.3.

## 8. File index

* `07_Day7_Working_Notes.md` — this document (Day-7 narrative, working level).
* `day7_sim/DATA_SHEET.md` — every citable number (H-1…H-22), iteration ladder, limitations.
* `day7_sim/results/` — `gate.json` (8/8), `S0–S7`, `S8_*`, `S9_optimized.json`, `S10_mc_ascent.json`, `S11_mc_recovery.json`, `R1–R5 json`, figs 1–13.
* `day7_sim/`: `params.py, atmosphere.py, vehicle.py, sim.py, studies.py, validate.py, plots.py, recovery_sim.py, run_recovery.py, doe.py, mc.py, plots2.py`, `README.md`.
* Finalized today: `05_Day5_Repair_and_Completion.md`; Day-6 deck v1.1 + `06_Day6_Addendum_v1_1.md` (from morning session).
