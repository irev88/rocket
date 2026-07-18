# Repository Structural Map & Reorganization Plan

**Date:** 18 July 2026 · **Branch:** `arena/019f7305-rocket`

---

**Status:** ✅ REORGANIZATION COMPLETE (18 July 2026) · All Days 1–7 materials reviewed, corrected, and finalized.

---

## 1. Project Overview

This repository contains a **10-day AI co-design program** (11–20 July 2026) to conceptually design a reusable launch vehicle. The program is structured as a multidisciplinary design optimization (MDO) exercise, graded on engineering *process* rather than product.

### Mission & Vehicle Summary

| Parameter | Value |
|---|---|
| Payload | 20,000 kg to Sun-Synchronous Orbit (500 km, 97.4°) |
| Vehicle | Two-stage LOX/RP-1, GLOM ≈ 600 t (baseline) |
| S1 Propulsion | 9× Merlin 1D-class (Octaweb), recoverable |
| S2 Propulsion | 1× Merlin Vacuum-class (expendable) |
| Recovery | Hybrid ocean net/cable catch (inspired by Long March 10B) |
| Cost Target | < $30M per launch, ≥ 10 flights/year |

### Two Closed Design Paths (Day 7–8 outcome)

| | Path A (Payload-Driven) | Path B (GLOM-Driven) |
|---|---|---|
| GLOM | 802 t (+34%) | 600 t (nominal) |
| Payload | 20 t SSO | 12 t SSO |
| S1 Engines | 12× M1D | 9× M1D |
| S2 Engines | 4× MVac | 2× MVac |
| Launch Cost | $37.6M | $24.4M |
| Specific Cost | $1,879/kg | $2,033/kg |

---

## 2. Current Repository Structure (As-Is)

```
rocket/
├── README.md                              ← Stub (9 bytes: "# rocket\n")
├── engineering_notebook.md                ← Consolidated decision log (Day 1–7)
│
│─── REPORTS & WORKING NOTES (flat, numbered) ──────────────────────────
├── 01_Project_Status_and_Critical_Review.md  ← Day-6 audit & forward plan
├── 02_Day6_Reusability_Strategy_DRAFT.md     ← SUPERSEDED (morning draft)
├── 02_Day6_Reusability_Strategy_FINAL.md     ← Day 6 FINAL report (45.8 KB)
├── 03_Day7_AI_Assisted_Optimization_FINAL.md ← Day 7 FINAL report (35.0 KB)
├── 04_Day6_Image_Prompts.md                  ← 6 AI image prompts for Day 6 deck
├── 05_Day5_Repair_and_Completion.md          ← Day 5 retirement record
├── 06_Day6_Addendum_v1_1.md                  ← Day 6 corrections post-Day-7 repair
├── 07_Day7_Working_Notes.md                  ← Day 7 working notes (superseded by FINAL)
├── 08_Day8_Reliability_and_Economics_FINAL.md ← Day 8 FINAL report (24.1 KB)
├── 09_Day9_System_Integration_FINAL.md        ← Day 9 FINAL report (23.6 KB)
│
│─── PRESENTATION DECKS (.pptx) ─────────────────────────────────────────
├── Day6_可重复使用策略_回收概念.pptx            ← Day 6 deck (1.05 MB, bilingual CN/EN)
├── Day7_AI_辅助优化_设计迭代.pptx               ← Day 7 deck (108 KB, bilingual CN/EN)
│   ⚠️ No PPTX for Day 8, Day 9, or Day 10
│
│─── SOURCE UPLOADS ─────────────────────────────────────────────────────
├── uploads/
│   ├── Summer Program.pdf                 ← Course blueprint/schedule
│   ├── Summer Program (5).pdf             ← Compiled program report (91 pp)
│   ├── master data.pdf                    ← OpenRocket trajectory export (10 pp)
│   ├── Presentation (1).pdf              ← Day 2 deck
│   ├── Day3-presentation.pdf             ← Day 3 deck
│   ├── Day 4 (1).pdf                     ← Day 4 deck
│   └── Day 5 (1).pdf                     ← Day 5 deck
│
│─── EXTRACTED TEXT (from PDFs) ──────────────────────────────────────────
├── extracted/
│   ├── Summer Program.txt                ← Blueprint text
│   ├── Summer Program (5).txt            ← Full report text (2,961 lines)
│   ├── master data.txt                   ← Trajectory table (60 lines)
│   ├── Presentation (1).txt             ← Day 2 deck text
│   ├── Day3-presentation.txt            ← Day 3 deck text
│   ├── Day 4 (1).txt                    ← Day 4 deck text
│   └── Day 5 (1).txt                    ← Day 5 deck text
│
│─── RENDERED IMAGES (from master data.pdf) ──────────────────────────────
├── rendered/
│   └── master_p1.png … master_p10.png    ← 10 page renders of master data
│
│─── DAY 6 ASSETS ────────────────────────────────────────────────────────
├── day6_assets/
│   ├── build_day6_ppt.py                 ← PPTX generation script (29.9 KB)
│   ├── audit_ppt_layout.py               ← Layout audit script
│   ├── svg_recovery_sequence.svg/.png    ← Recovery sequence diagram
│   ├── svg_catch_loadpath.svg/.png       ← Catch load-path diagram
│   ├── svg_hover_slam.svg/.png           ← Hover-slam ignition window
│   └── svg_reserve_closure.svg/.png      ← Reserve closure diagram
│
│─── DAY 7 SIMULATION SUITE ──────────────────────────────────────────────
└── day7_sim/
    ├── params.py           (123 lines)   ← Constants, Day 1–4 traceability
    ├── atmosphere.py        (67 lines)   ← USSA76 exponential layers
    ├── vehicle.py           (75 lines)   ← Isp(h), thrust, Cd(Mach)
    ├── sim.py              (358 lines)   ← 3-DOF RK4 ascent integrator
    ├── studies.py          (306 lines)   ← S0–S7 study suites
    ├── validate.py         (108 lines)   ← 8-gate audit (8/8 PASS)
    ├── recovery_sim.py     (188 lines)   ← 2-DOF descent chain
    ├── run_recovery.py     (313 lines)   ← R1–R5 recovery analyses
    ├── doe.py              (183 lines)   ← Latin Hypercube DOE
    ├── mc.py               (181 lines)   ← Monte-Carlo ascent + recovery
    ├── plots.py            (215 lines)   ← fig1–fig6
    ├── plots2.py           (167 lines)   ← fig7–fig13
    ├── tune_kick.py         (51 lines)   ← Superseded kick tuner
    ├── build_day7_ppt.py   (504 lines)   ← PPTX generation for Day 7
    ├── DATA_SHEET.md                     ← Citable reference numbers (H-1…H-22)
    ├── README.md                         ← Run instructions
    └── results/
        ├── 34 × *.json                  ← Machine-readable results
        ├── 13 × fig*.png                ← Generated plots
        ├── gate.json                    ← 8/8 PASS validation
        └── doe_log.txt                  ← DOE execution log
```

**Statistics:** ~2,839 lines of Python · 34 JSON result files · 13 figures · 10 report/note files · 2 PPTX decks · 7 source PDFs

---

## 3. Critical Assessment of Completed Work

### ✅ What Has Been Done Well

1. **Rigorous physics repair (Day 5→7).** The identification of "phantom energy" (effective Isp 364/427 s vs declared 282/348 s) and the rebuild of a 3-DOF integrator with honesty rules is an outstanding engineering catch. The 8-gate validation is thorough.

2. **Complete design-iteration ladder (Day 7).** Six iterations traced from the retired baseline through margin recovery, thrust-to-weight repair, expendable analysis, and architecture-level rescaling — this is textbook systems engineering.

3. **Recovery sub-problem closure.** The fixed-point reserve analysis (R* = 30–37 t) and Monte-Carlo verification (P ≥ 0.95 at 34.5 t) closes the recovery corridor with statistical rigor.

4. **Economic model with path trade (Day 8).** Two closed baselines with full cost decomposition and a specific-cost inversion insight (Path A cheaper per kg despite higher per-launch cost).

5. **Cross-document traceability.** The Consistency Register (CR-D7-01 through CR-D7-07) and the Day 9 Traceability Matrix ensure no claim floats without verification.

6. **Comprehensive FMEA.** 10 failure modes with RPN before/after mitigation, calibrated against operational flight heritage.

### 🔴 Critical Gaps and Issues

| # | Gap | Severity | Impact |
|---|---|---|---|
| **G-1** | **Day 10 competition deck does not exist** | 🔴 Critical | This is the final graded deliverable. Days 1–9 content is meaningless without a cohesive defense presentation. |
| **G-2** | **No PPTX for Day 8 or Day 9** | 🟠 Major | Pattern from Days 1–7 requires a bilingual deck per day. Days 8–9 break this pattern. |
| **G-3** | **Day 7 PPTX likely not updated with final simulation results** | 🟠 Major | The 108 KB Day7 PPTX was likely built before the full Monte-Carlo/DOE results were available. |
| **G-4** | **Repository structure is flat and disorganized** | 🟡 Moderate | 10+ numbered files at root with inconsistent prefixes; superseded drafts mixed with finals; no clear separation of code/docs/data. |
| **G-5** | **FIGURE placeholders in Day 6 FINAL report** | 🟡 Moderate | "[FIGURE 1 — REQUIRED]", "[FIGURE 2 — REQUIRED]" etc. appear throughout but are never filled. SVG assets exist in `day6_assets/` but are not linked. |
| **G-6** | **No CAD sketches or vehicle diagrams** | 🟡 Moderate | The blueprint (§3) calls for CAD sketches. The report has "Figure N:" captions with no images (Figures 1–5 in Day 4). |
| **G-7** | **6 AI image prompts defined but never executed** | 🟡 Moderate | `04_Day6_Image_Prompts.md` defines 6 photorealistic images for the Day 6 deck but none have been generated. |
| **G-8** | **Engineering notebook stops at Day 7** | 🟡 Moderate | `engineering_notebook.md` documents Days 1–7 but omits Days 8–9 decisions. |
| **G-9** | **Day 5 presentation errors (from MINOR-6) not fixed** | 🟡 Moderate | Mass table mismatches, date errors, propellant mappings, "over 400+ landings" vs 637th — flagged but not corrected in source decks. |
| **G-10** | **Path A vs Path B decision not made** | 🟢 Low | Day 8 delivers two paths; Day 9 presents both for defense. But no recommendation on which to lead with on Day 10. |

---

## 4. Proposed Reorganized Structure (To-Be)

```
rocket/
│
├── README.md                          ← Comprehensive project README
├── REPO_MAP.md                        ← This document
├── engineering_notebook.md            ← Central decision log (extend through Day 10)
│
├── docs/
│   ├── blueprint/
│   │   ├── summer_program.md          ← Course overview/schedule
│   │   └── summer_program_full.md     ← Full 91-page compiled report
│   │
│   ├── reports/
│   │   ├── day06_reusability_strategy.md    ← FINAL report
│   │   ├── day07_trajectory_optimization.md ← FINAL report
│   │   ├── day08_reliability_economics.md   ← FINAL report
│   │   ├── day09_system_integration.md      ← FINAL report
│   │   └── day10_competition.md             ← Day 10 FINAL (TO CREATE)
│   │
│   ├── working_notes/
│   │   ├── project_status_review.md         ← Day-6 audit (01_*.md)
│   │   ├── day05_repair_record.md           ← Day 5 retirement
│   │   ├── day06_addendum_v1.1.md           ← Post-repair corrections
│   │   ├── day07_working_notes.md           ← Pre-final working notes
│   │   └── day06_superseded_draft.md        ← Kept for audit trail
│   │
│   └── image_prompts/
│       └── day06_image_prompts.md           ← 6 AI image prompt definitions
│
├── presentations/
│   ├── day02_rocket_fundamentals.pptx       ← From uploads/
│   ├── day03_propulsion.pptx               ← From uploads/
│   ├── day04_mass_budget.pptx              ← From uploads/
│   ├── day05_trajectory.pptx               ← From uploads/
│   ├── day06_reusability.pptx              ← Regenerated v1.1
│   ├── day07_optimization.pptx             ← Updated with final results
│   ├── day08_reliability.pptx              ← TO CREATE
│   ├── day09_integration.pptx              ← TO CREATE
│   └── day10_competition.pptx              ← TO CREATE (final defense)
│
├── simulations/
│   └── day7_sim/                          ← Full simulation suite (unchanged)
│       ├── params.py
│       ├── atmosphere.py
│       ├── vehicle.py
│       ├── sim.py
│       ├── studies.py
│       ├── validate.py
│       ├── recovery_sim.py
│       ├── run_recovery.py
│       ├── doe.py
│       ├── mc.py
│       ├── plots.py
│       ├── plots2.py
│       ├── build_day7_ppt.py
│       ├── DATA_SHEET.md
│       ├── README.md
│       └── results/
│           ├── *.json (34 files)
│           ├── fig*.png (13 files)
│           └── gate.json
│
├── assets/
│   ├── diagrams/                          ← SVG/PNG technical diagrams
│   │   ├── svg_recovery_sequence.svg/.png
│   │   ├── svg_catch_loadpath.svg/.png
│   │   ├── svg_hover_slam.svg/.png
│   │   └── svg_reserve_closure.svg/.png
│   ├── scripts/
│   │   ├── build_day6_ppt.py
│   │   └── audit_ppt_layout.py
│   └── rendered/                          ← OpenRocket page renders
│       └── master_p1.png … master_p10.png
│
├── data/
│   ├── source/                            ← Original uploaded PDFs
│   │   ├── Summer Program.pdf
│   │   ├── Summer Program (5).pdf
│   │   ├── master data.pdf
│   │   ├── Presentation (1).pdf
│   │   ├── Day3-presentation.pdf
│   │   ├── Day 4 (1).pdf
│   │   └── Day 5 (1).pdf
│   └── extracted/                         ← Text extracted from PDFs
│       ├── summer_program.txt
│       ├── summer_program_full.txt
│       ├── master_data.txt
│       ├── day2_presentation.txt
│       ├── day3_presentation.txt
│       ├── day4_presentation.txt
│       └── day5_presentation.txt
│
└── .gitignore                             ← Ignore __pycache__, *.pyc, etc.
```

### Key Reorganization Principles

1. **Separate concerns:** Reports, presentations, simulation code, assets, and source data each get their own directory.
2. **Number consistently:** Use `dayNN_` prefix (zero-padded) for all day-specific artifacts.
3. **Final vs working:** Separate `reports/` (final only) from `working_notes/` (audit trail).
4. **Renamed extracted files:** Remove spaces and parenthetical numbers for clean paths.
5. **Simulation suite stays together:** `day7_sim/` moves under `simulations/` as a self-contained unit.
6. **Source data is immutable:** `data/source/` holds uploads; `data/extracted/` holds derived text.

---

## 5. Completion Status by Day

| Day | Date | Theme | Status | Key Remaining Work |
|---|---|---|---|---|
| 1 | 11 Jul | Mission Definition | ✅ Complete | None |
| 2 | 12 Jul | Rocket Fundamentals | ✅ Complete | Fix deck date error (7/11 → 7/12) |
| 3 | 13 Jul | Propulsion System | ✅ Complete | Fix propellant mapping errors in deck |
| 4 | 14 Jul | Mass Budget & Materials | ✅ Complete | Fill Figure placeholders; fix deck date |
| 5 | 15 Jul | Aerodynamics & Trajectory | ✅ Retired | Physics invalidated; superseded by Day 7 |
| 6 | 16 Jul | Reusability Strategy | ✅ Complete | Fill FIGURE placeholders; generate 6 AI images |
| 7 | 17 Jul | AI-Assisted Optimization | ✅ Complete | Verify PPTX matches final results |
| 8 | 18 Jul | Reliability & Economics | ✅ Report done | **Create PPTX deck** |
| 9 | 19 Jul | System Integration | ✅ Report done | **Create PPTX deck** |
| **10** | **20 Jul** | **Design Competition** | **❌ NOT STARTED** | **Create competition deck + defense prep** |

---

## 6. Recommended Next Steps (Priority-Ordered)

### 🔴 IMMEDIATE (Critical Path for Day 10)

1. **Create Day 10 Competition Deck**
   - Narrative arc: Requirement → Architecture → Verified Performance → Recovery Innovation → Economics → Defense
   - Lead with the LM 10B-validated catch concept and "Reuse Passport" sensor system
   - Present both Path A and Path B with the economic trade table
   - Include the 8-question Red Team Q&A from Day 9

2. **Create Day 8 PPTX Deck**
   - Cost model waterfall charts
   - FMEA table (condensed to key 5 failure modes)
   - RBD diagram
   - Over-acceleration mitigation trade

3. **Create Day 9 PPTX Deck**
   - Traceability matrix (visual)
   - Consistency register resolution summary
   - System flowchart (already in text form)

### 🟠 HIGH PRIORITY

4. **Update Day 7 PPTX** with final Monte-Carlo and DOE results if not already included
5. **Fill Figure placeholders** in Day 6 FINAL report — the SVG assets already exist in `day6_assets/`
6. **Generate the 6 AI images** from `04_Day6_Image_Prompts.md` for deck enrichment
7. **Extend engineering notebook** through Days 8–9

### 🟡 MEDIUM PRIORITY

8. **Execute the reorganization** — move files into the proposed structure
9. **Fix known deck errors** (dates, mass tables, propellant mappings per MINOR-6)
10. **Add vehicle schematic diagrams** for the CAD-sketch requirement

### 🟢 LOWER PRIORITY

11. **Update README.md** with project overview
12. **Add .gitignore** for Python artifacts
13. **Cross-link all documents** with consistent relative paths

---

## 7. Dependency Graph — What Feeds What

```
Day 1 (Requirements) ──────────────────────────────────────────────┐
    │                                                               │
    ├── Day 2 (Sizing) ──→ Day 3 (Propulsion) ──→ Day 4 (Mass/Mat) │
    │       │                                              │        │
    │       └──────────────────────────────────────→ Day 5 (Traj)  │
    │                                              (RETIRED)       │
    │                                                  │           │
    │       ┌──────────────────────────────────────────┘           │
    │       │                                                       │
    │   Day 6 (Recovery) ←── Day 4 architecture                    │
    │       │                                                       │
    │   Day 7 (Optimization) ──→ Repairs Day 5; feeds Day 6/8      │
    │       │                                                       │
    │       ├── Ascent: deficit 2,088 m/s → iteration ladder        │
    │       ├── Recovery: reserve 18 t → 34.5 t                     │
    │       ├── DOE: 1,200 LHS samples                              │
    │       └── Monte-Carlo: P_survival 0.38–0.95                   │
    │               │                                               │
    │   Day 8 (Economics) ←── Day 7 closed baselines                │
    │       │                                                       │
    │       ├── Path A: 802 t / 20 t / $37.6M / $1,879/kg          │
    │       └── Path B: 600 t / 12 t / $24.4M / $2,033/kg          │
    │               │                                               │
    │   Day 9 (Integration) ←── All above                           │
    │       │                                                       │
    │       ├── Traceability matrix                                 │
    │       ├── CR register resolution                              │
    │       └── Red Team Q&A                                        │
    │               │                                               │
    └─── Day 10 (Competition) ←── All above ←──────────────────────┘
              │
              └── Final defense presentation (TO CREATE)
```

---

## 8. File Inventory Summary

| Category | Count | Total Size |
|---|---:|---:|
| Python code (day7_sim) | 14 files | 2,839 lines |
| JSON results | 34 files | ~1 MB |
| PNG figures | 13 plots + 10 renders + 4 SVG renders | ~1.7 MB |
| Markdown reports | 10 files | ~180 KB |
| PPTX decks | 2 current + 5 uploads | ~2.3 MB |
| PDF source documents | 7 files | ~8 MB |
| Extracted text | 7 files | ~230 KB |
| **Total** | **~90 files** | **~12 MB** |

---

*This document serves as both a structural audit and a reorganization blueprint. The proposed structure prioritizes clarity for the Day 10 competition preparation while maintaining full audit traceability.*
