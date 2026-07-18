# AI Co-Design of a Reusable Launch Vehicle

**Program Window:** 11–20 July 2026 · **Branch:** `arena/019f7305-rocket`  
**Engineering Copilot:** Arena.ai Agent Mode · **Chief Engineer:** Prof. Xu  
**Subsystem Mentors:** Yingjie & Jingjie (CASC Graduate Mentors)

---

## Overview

This repository documents a **10-day multidisciplinary design optimization (MDO) exercise** to conceptually design a reusable two-stage kerolox launch vehicle, performed with an LLM as engineering copilot. The program emphasizes engineering *process* — requirements decomposition, trade-off analysis, uncertainty quantification, and cross-document traceability — over "the best rocket."

**Days 1–7 are complete.** Days 8–9 reports are finalized. Day 10 (final competition deck) is pending.

---

## Mission & Vehicle

| Parameter | Value |
|---|---|
| **Payload** | 20,000 kg to Sun-Synchronous Orbit (500 km, 97.4° inclination) |
| **Propellant** | LOX/RP-1 (both stages) |
| **GLOM** | 600 t (baseline) — see [Closure Paths](#closure-paths) |
| **S1 Propulsion** | 9× Merlin 1D-class (Octaweb), recoverable via hybrid ocean catch |
| **S2 Propulsion** | 1× Merlin Vacuum-class (expendable) |
| **Recovery** | Downrange ocean net/cable capture (vessel ~489 km downrange) |
| **Cost Target** | < $30M per launch, ≥ 10 flights/year |

### Closure Paths (Day 7–8 outcome)

After repairing the trajectory physics on Day 7, two physically closed baselines emerged:

| | **Path A** (Payload-Driven) | **Path B** (GLOM-Driven) |
|---|---|---|
| GLOM | 802 t (+34%) | 600 t |
| Payload to SSO | 20,000 kg | 12,000 kg |
| S1 / S2 Engines | 12× M1D / 4× MVac | 9× M1D / 2× MVac |
| Launch Cost (N=15) | $37.65M | $24.45M |
| Specific Cost | $1,883/kg | $2,038/kg |
| Recovery Reserve | 34.5 t | 34.5 t |

---

## Repository Structure

```
rocket/
├── README.md                    ← This file
├── engineering_notebook.md      ← Central decision log (Days 1–7, with closing summary)
├── .gitignore
│
├── docs/
│   ├── REPO_MAP.md              ← Structural audit & reorganization plan
│   ├── CRITICAL_REVIEW_LOG.md   ← All issues found & fixed during review
│   ├── blueprint/               ← Course schedule materials
│   ├── reports/                 ← Finalized day reports
│   │   ├── day06_reusability_strategy.md      (Day 6 — FINAL)
│   │   ├── day07_trajectory_optimization.md   (Day 7 — FINAL)
│   │   ├── day08_reliability_economics.md     (Day 8 — FINAL)
│   │   └── day09_system_integration.md        (Day 9 — FINAL)
│   ├── working_notes/           ← Audit trail, addenda, superseded drafts
│   │   ├── project_status_review.md           (Day 6 critical audit)
│   │   ├── day05_repair_record.md             (Day 5 retirement record)
│   │   ├── day06_addendum_v1.1.md             (Post-Day-7 corrections)
│   │   ├── day07_working_notes.md             (Pre-final working notes)
│   │   └── day06_superseded_draft.md          (Morning draft, superseded)
│   └── image_prompts/           ← AI image generation prompts
│       └── day06_image_prompts.md
│
├── presentations/
│   ├── day06_reusability.pptx   ← Day 6 deck (15 slides, bilingual CN/EN)
│   └── day07_optimization.pptx  ← Day 7 deck (20 slides, bilingual CN/EN)
│
├── simulations/
│   └── day7_sim/                ← Full trajectory & recovery simulation suite
│       ├── params.py            ← All Day 1–4 constants with traceability
│       ├── atmosphere.py        ← USSA76 exponential layers
│       ├── vehicle.py           ← Isp(h), thrust, Cd(Mach)
│       ├── sim.py               ← 3-DOF RK4 ascent integrator
│       ├── recovery_sim.py      ← 2-DOF descent chain
│       ├── studies.py           ← S0–S7 study suites
│       ├── validate.py          ← 8-gate audit (8/8 PASS)
│       ├── doe.py               ← Latin Hypercube DOE (1,200 samples)
│       ├── mc.py                ← Monte-Carlo (800 ascent + 1,000 recovery)
│       ├── run_recovery.py      ← R1–R5 recovery analyses
│       ├── plots.py / plots2.py ← fig1–fig13
│       ├── build_day7_ppt.py    ← Day 7 PPTX generator
│       ├── DATA_SHEET.md        ← Citable reference numbers (H-1 to H-22)
│       └── results/             ← 34 JSON files + 13 figures + gate.json
│
├── assets/
│   ├── diagrams/                ← SVG/PNG technical schematics
│   ├── scripts/                 ← PPTX build scripts (Day 6)
│   └── rendered/                ← OpenRocket page renders (master data)
│
└── data/
    ├── source/                  ← Original uploaded PDFs (immutable)
    └── extracted/               ← Text extracted from PDFs
```

## Progress Status

| Day | Date | Theme | Status | Key Artifact |
|---|---|---|---|---|
| 1 | 11 Jul | Mission Definition | ✅ Complete | `engineering_notebook.md` §1 |
| 2 | 12 Jul | Rocket Fundamentals | ✅ Complete | `engineering_notebook.md` §2 |
| 3 | 13 Jul | Propulsion System | ✅ Complete | `engineering_notebook.md` §3 (+engine-out analysis) |
| 4 | 14 Jul | Mass Budget & Materials | ✅ Complete | `engineering_notebook.md` §4 |
| 5 | 15 Jul | Aerodynamics & Trajectory | ⚠️ Retired | `docs/working_notes/day05_repair_record.md` |
| 6 | 16 Jul | Reusability Strategy | ✅ Complete | `docs/reports/day06_reusability_strategy.md` |
| 7 | 17 Jul | AI-Assisted Optimization | ✅ Complete | `docs/reports/day07_trajectory_optimization.md` |
| 8 | 18 Jul | Reliability & Economics | ✅ Complete | `docs/reports/day08_reliability_economics.md` |
| 9 | 19 Jul | System Integration | ✅ Complete | `docs/reports/day09_system_integration.md` |
| **10** | **20 Jul** | **Design Competition** | **⬜ Pending** | *To create* |

## Key Engineering Findings

1. **Day 5 trajectory retired** — OpenRocket data contained "phantom energy" (implied Isp 364/427 s vs. declared 282/348 s kerolox physics). Rebuilt with honest 3-DOF integrator, 8/8 validation gates.
2. **2,088 m/s orbital deficit** — The 600 t / 20 t SSO configuration cannot reach orbit under honest physics. Guidance optimization (DE, 1,200 LHS samples) confirms the deficit is structural, not tunable.
3. **Recovery reserve 2× undersized** — 18 t → 34.5 t required (Monte-Carlo verified, P ≥ 0.95 under atmospheric dispersions).
4. **Two closed paths** — Path A (802 t / 20 t) or Path B (600 t / 12 t), both with 34.5 t recovery reserve.
5. **Structural over-acceleration** — 2× MVac config hits 6.2–6.4 g at SECO; resolved with 40% throttle near burnout (payload penalty <1%).
6. **Engine-out capability** — 9-engine Octaweb permits 1 EDO at liftoff (T/W = 1.15); 2+ EDO forces abort. Payload penalty ~4 t.

## Running the Simulation

```bash
cd simulations/day7_sim
python3 studies.py          # S0–S7 suites → results/*.json (~3 min)
python3 validate.py         # 8-gate audit → results/gate.json (8/8 PASS)
python3 plots.py            # fig1–fig6 → results/fig*.png
python3 run_recovery.py     # R1–R5 recovery chain (~2 min)
python3 doe.py              # DOE + optimization (~25 min)
python3 mc.py               # Monte-Carlo ascent + recovery (~3 min)
python3 plots2.py           # fig7–fig13
```

## Reading Order

For a coherent understanding of the project:

1. Start with `engineering_notebook.md` — the central decision log covering Days 1–7
2. Read the Day 7 report (`docs/reports/day07_trajectory_optimization.md`) for the full technical depth
3. Read the Day 8 report (`docs/reports/day08_reliability_economics.md`) for economics and risk
4. Read the Day 9 report (`docs/reports/day09_system_integration.md`) for the final integration and Q&A
5. See `docs/CRITICAL_REVIEW_LOG.md` for all issues found and fixed during the review cycle

## Source Documents

The original course materials are preserved immutably in `data/source/`:
- `summer_program.pdf` — Course blueprint and schedule
- `summer_program_full.pdf` — Compiled 91-page program report (Days 1–5)
- `master_data.pdf` — OpenRocket trajectory export (retired, superseded by `simulations/day7_sim/`)
- `day2_presentation.pdf` through `day5_presentation.pdf` — Original bilingual decks

See `engineering_notebook.md` Appendix A for a complete list of known errors in the original source decks.

## Engineering Integrity

Every numerical value in this repository traces to either:
- (a) A Day 1–4 documented parameter,
- (b) Our own simulation output (`simulations/day7_sim/results/`), or
- (c) A cited external source used exclusively for validation (never as model input).

The design baseline is physically honest, mathematically closed, and fully traceable.
