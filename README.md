# AI Co-Design of a Reusable Launch Vehicle

**Program Window:** 11–20 July 2026 · **Branch:** `arena/019f7305-rocket`  
**Engineering Copilot:** Arena.ai Agent Mode · **Chief Engineer:** Prof. Xu  
**Subsystem Mentors:** Yingjie & Jingjie (CASC Graduate Mentors)

---

## Overview

A 10-day multidisciplinary design optimization (MDO) exercise to conceptually design a reusable two-stage kerolox launch vehicle, performed with an LLM as engineering copilot. The program emphasizes engineering *process* — requirements decomposition, trade-off analysis, uncertainty quantification, and cross-document traceability.

**Days 1–8 are complete** with reports, presentations, and verified simulation data. Day 10 (final competition) is pending.

---

## Day-by-Day Deliverables

Each day's folder under `days/` contains its report, presentation, and reference materials:

| Day | Date | Theme | Report | Presentation | Status |
|---|---|---|---|---|---|
| 1 | 11 Jul | Mission Definition | `days/day01_.../report.md` | — | ✅ |
| 2 | 12 Jul | Rocket Fundamentals | `days/day02_.../report.md` | `presentation.pdf` | ✅ |
| 3 | 13 Jul | Propulsion System | `days/day03_.../report.md` | `presentation.pdf` | ✅ |
| 4 | 14 Jul | Mass Budget & Materials | `days/day04_.../report.md` | `presentation.pdf` | ✅ |
| 5 | 15 Jul | Aerodynamics & Trajectory | `days/day05_.../report.md` | `presentation.pdf` (retired data) | ⚠️ Retired |
| 6 | 16 Jul | Reusability Strategy | `days/day06_.../full_report.md` | `presentation.pptx` (15 slides) | ✅ |
| 7 | 17 Jul | Trajectory Optimization | `days/day07_.../full_report.md` | `presentation.pptx` (20 slides) | ✅ |
| 8 | 18 Jul | Reliability & Economics | `days/day08_.../full_report.md` | `presentation.pptx` (9 slides) | ✅ |
| 9 | 19 Jul | System Integration | `docs/reports/day09_...md` | — | ✅ Report only |
| **10** | **20 Jul** | **Competition** | — | — | **⬜ Pending** |

---

## Vehicle & Mission

| Parameter | Value |
|---|---|
| **Payload** | 20,000 kg to SSO (500 km, 97.4°) |
| **Propellant** | LOX/RP-1 (both stages) |
| **GLOM** | 600 t baseline → 802 t scaled (Path A) |
| **S1** | 9× Merlin 1D (recoverable via ocean net catch) |
| **S2** | 1× Merlin Vacuum (expendable) |
| **Recovery** | Downrange hybrid catch, vessel ~489 km downrange, 34.5 t reserve |

### Two Closed Paths (Day 7–8)

| | Path A | Path B |
|---|---|---|
| GLOM | 802 t | 600 t |
| Payload | 20 t SSO | 12 t SSO |
| Cost (N=15) | $37.65M | $24.45M |
| Specific Cost | $1,883/kg | $2,038/kg |

---

## Repository Structure

```
rocket/
├── README.md                       ← This file
├── engineering_notebook.md         ← Central decision log (Days 1–7, with closing summary)
├── .gitignore
│
├── days/                           ← ★ Day-by-day deliverables
│   ├── day01_mission_definition/   (report + reference)
│   ├── day02_rocket_fundamentals/  (report + presentation.pdf + reference)
│   ├── day03_propulsion/           (report + presentation.pdf + reference)
│   ├── day04_mass_budget/          (report + presentation.pdf + reference)
│   ├── day05_trajectory/           (report + presentation.pdf + OpenRocket data)
│   ├── day06_reusability/          (full_report + presentation.pptx + diagrams/)
│   ├── day07_optimization/         (full_report + presentation.pptx + figures/)
│   └── day08_reliability_economics/(full_report + presentation.pptx + build script)
│
├── docs/                           ← Cross-cutting documents
│   ├── reports/day09_...           (Day 9 system integration report)
│   ├── working_notes/              (audit trail, addenda, superseded drafts)
│   ├── CRITICAL_REVIEW_LOG.md      (all issues found & fixed)
│   └── REPO_MAP.md                 (structural audit)
│
├── simulations/day7_sim/           ← Full simulation suite (2,839 lines Python)
│   ├── params.py, sim.py, recovery_sim.py, doe.py, mc.py, validate.py ...
│   ├── DATA_SHEET.md               (H-1 to H-22 citable numbers)
│   └── results/                    (34 JSON + 13 figures + gate.json 8/8 PASS)
│
├── presentations/                  ← Generated PPTX decks
├── assets/                         (diagrams/, scripts/, rendered/)
└── data/source/                    ← Original uploaded PDFs (immutable)
```

---

## Reading Order

1. **Start here:** `engineering_notebook.md` — the central narrative from Day 1–7 with full decision log
2. **Deep dive:** `days/day07_optimization/full_report.md` — the core technical achievement (trajectory repair + optimization)
3. **Economics:** `days/day08_reliability_economics/full_report.md` — cost model, FMEA, RBD
4. **Integration:** `docs/reports/day09_system_integration.md` — traceability matrix + Red Team Q&A
5. **Review log:** `docs/CRITICAL_REVIEW_LOG.md` — all 9 issues found and fixed during critical review

## Simulation

```bash
cd simulations/day7_sim
python3 validate.py    # 8-gate audit → 8/8 PASS
python3 studies.py     # S0–S7 study suites
python3 run_recovery.py  # R1–R5 recovery chain
python3 doe.py         # 1,200 LHS sensitivity + DE optimization
python3 mc.py          # Monte-Carlo (800 ascent + 1,000 recovery)
```

## Engineering Integrity

Every numerical value traces to either: (a) a Day 1–4 documented parameter, (b) our own simulation output (`simulations/day7_sim/results/`), or (c) a cited external source used exclusively for validation. The design baseline is physically honest, mathematically closed, and fully traceable.
