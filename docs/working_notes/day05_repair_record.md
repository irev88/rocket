# Day 5 (Aerodynamics & Trajectory) — Repair and Completion Record

**Status: COMPLETED (repaired)** · Issued 2026-07-17 (Day 7) · Supersedes the trajectory results of `Summer Program (5).pdf` §2.5–2.7 and `master data.pdf`, which are formally **retired** (physics-invalid).

---

## 1. Why the Day 5 model was retired

| # | Defect (audit ref) | Evidence |
|---|---|---|
| D1 | **Energy non-conservation (C-1)** | Old data implies effective Isp: S1 ≈ **364 s** (envelope 282–311), S2 ≈ **427 s** (declared 348) — re-derived with the repaired model's honest losses (`simulations/day7_sim/results/S0_audit_implied_isp.json`). S2 gained 5,080 m/s vs its own Tsiolkovsky bound ~4,620 m/s. |
| D2 | **Orbit not closed, unflagged (C-2)** | Final 245.5 km / 7,610 m/s ⇒ perigee −248 km (suborbital), yet reported as mission success. |
| D3 | **Max-Q misreported (M-3)** | Claimed ~28 kPa @ 12–15 km; the model's *own* table shows **40.4 kPa @ t+60 s / 9.3 km / Mach 1.24**. |
| D4 | **Internal inconsistency** | Master data `v` column cannot be integrated from its own `acceleration` column anywhere in t=0–150 s (e.g., stated accel 2.9→6.9 m/s² averages ≤4.9 yet Δv=420 m/s ⇒ 7.0 required). Velocity column is inflated throughout S1 as well. |
| D5 | **Wrong tool** | OpenRocket (hobby-model-rocketry code) applied to a 600 t orbital launcher; its own "next steps" admitted S2 validation was still pending. |

The mass bookkeeping was the only sound element (58 t staging drop; 39/37.2 t finals) — retained as the Day-6/7 reference.

## 2. Repaired model (acceptance gate 8/8 PASS)

Rebuilt from scratch in `simulations/day7_sim/` (RK4, spherical Earth, USSA76 atmosphere, Isp(h) with vacuum-value ceiling, explicit S2 loft guidance, q/g tracked every step). Gate G1–G8 all PASS (`simulations/day7_sim/results/gate.json`): Isp in-envelope, mass closure exact, energy-balance residual **3 m/s**, MECO/Max-Q inside real-flight family bands (Mach 5.7 @ 66.5 km; Q 31.2 kPa @ t+70 s — F9-class consistent).

## 3. Honest replacement numbers (supersede Day 5 tables)

| Quantity | Retired Day 5 value | **Day-7 honest value** |
|---|---|---|
| Max-Q | "≈28 kPa @ 12–15 km (claim)" / 40.4 kPa (own data) | **31.2 kPa @ t+70 s / 11.0 km / Mach 1.41** |
| Staging (MECO) | 78 km / 2,520 m/s / Mach 8.2 / T+150 s | **66.5 km / 1,892 m/s / Mach 5.7 / γ 41° / T+142 s** |
| S1 gravity / drag losses | not decomposed | 1,217 / 26 m/s |
| S2 achieved Δv | 5,080 m/s (phantom) | **4,714 m/s** (bound 4,740 ✓) |
| Final state | "245.5 km / 7,610 m/s success" | SECO 78 km* / 5,939 m/s → perigee −3,823 km (**honest deficit 2,088 m/s** to 500×500) |
| Total "capability" | "11.1 km/s" | **ideal 7,875 m/s** (vs recorded requirement 11,000 m/s — the requirement itself carries ≈+1,100–1,400 m/s padding over physical need) |
| Δv margin | "+0.1 km/s" | **≈ −2.1 km/s at 20 t SSO** |

*SECO-endgame arc sag is a guidance-family artifact (see DATA_SHEET §5.2); energetically accounted.

## 4. Day 5's own "next steps" checklist — closure status

| Day 5 stated next step | Status | Where |
|---|---|---|
| 直径/阻力/储备推进剂灵敏度分析 (diameter / drag / reserve-prop sensitivity) | ✅ **Closed** | Cd ±20 % ⇒ drag loss 17–47 m/s, deficit shift ≤ 12 m/s (second-order; 3.9 m diameter retained). Reserve sensitivity ⇒ margin→prop study (deficit 2,088 → 1,467) |
| 用外部轨迹模型验证二级入轨 (external trajectory verification of S2 insertion) | ✅ **Closed** | Rebuilt model; orbit non-closure quantified (deficit 2,088 m/s; capability ≈ 6.6 t reusable at 600 t) |
| 细化回收段与分离后一级状态 (refine recovery segment / post-separation S1 state) | ✅ **Closed (V-1)** | Separation state delivered to Day 6/8 (T+142 s, 66.5 km, 1,892 m/s, γ 41°, downrange 51 km) |
| Further: entry-segment aero/thermal detail, guidance-quality optimization (collocation/PEG), dispersion Monte-Carlo | ➡ **Open — Day 7/8 scope** | flagged as follow-on tasks B3/B5, not Day-5 blockers anymore |

## 5. What this changes downstream (pointers)

- **Day 6**: recovery-side conclusions stand; ascent-fed numbers corrected via addendum v1.1 (`docs/working_notes/day06_addendum_v1.1.md`).
- **Day 7**: proceeds on the repaired model (Arc B/C per plan).
- **Day 8**: architecture decision package awaiting (iteration ladder: 600 t ≈ 6.6 t reusable · 2× MVac ≈ 12 t · expendable 2× ≈ 14 t · scaled family f≈1.39 ⇒ 20 t closed at ≈802 t GLOM).

*All values reproducible: `cd simulations/day7_sim && python3 studies.py && python3 validate.py && python3 plots.py` → `results/`*
