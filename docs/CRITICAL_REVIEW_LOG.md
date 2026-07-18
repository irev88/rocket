# Critical Review Log — Days 1–7 Materials

**Date:** 18 July 2026 · **Reviewer:** Arena.ai Agent (critical self-review)

---

## Summary

A systematic critical review of all Days 1–7 documents, simulation code, and numerical results was conducted. The review checked mathematical correctness, physical consistency, cross-document traceability, and logical coherence. **9 issues were identified and fixed** (committed); **6 additional items are noted as suggestions for future improvement** where execution would require significant additional work.

---

## Issues Fixed (Committed)

### FIX-1: Recovery Probability Arithmetic Error (Day 8) 🔴
- **Location:** `docs/reports/day08_reliability_economics.md` §3.2, Abstract
- **Error:** The report states $P_{\text{recovery}} = 95.1\%$, but the exact product of the stated component reliabilities gives:
  $$0.982 \times 0.990 \times 0.995 \times 0.988 \times 0.993 = 0.9490 = 94.9\%$$
- **Fix:** Corrected to 94.9% throughout the report (Abstract, §3.2, equation 3.4).
- **Impact:** Low (0.2 percentage points). Does not change any conclusions; the 5% insurance premium factor remains valid.

### FIX-2: Day 9 Q-5 Hover-Slam T/W Calculation Error 🔴
- **Location:** `docs/reports/day09_system_integration.md` Q-5 defense
- **Error:** The answer claimed "minimum thrust-to-weight ratio near touchdown is ≈1.8 (338 kN thrust / 185 kN booster mass at burnout)." The 185 kN figure has no basis — the near-empty booster weighs 410–441 kN, not 185 kN.
- **Correct physics:** At the 40% *design* throttle floor, SL thrust is 338 kN, giving T/W = 338/410 = 0.82 (below 1.0, technically permitting hover). The hover-slam commitment arises because the *operational* throttle floor (50–57%) produces thrust of 422–482 kN, which exceeds vehicle weight.
- **Fix:** Rewrote Q-5 answer with correct physical chain of reasoning.

### FIX-3: CR-D7-06 Reserve Savings Claim Not Corrected in Source (Day 6) 🟠
- **Location:** `docs/reports/day06_reusability_strategy.md` §3.3 and §10
- **Error:** Two passages still claimed the catch system "frees 6,000 kg of reserve propellant" / "releases 6 t of reserve versus the legged fallback." Day 7's descent simulation proved the reserve requirement is driven by entry ballistics (identical for both configurations) and is ≥34.5 t regardless.
- **Fix:** Added explicit "(Day 7 addendum:...)" annotations to both passages, withdrawing the reserve saving claim while retaining the valid 2.5 t hardware saving.
- **Note:** The Day 6 PPTX build script was already corrected in the previous commit.

### FIX-4: Day 8 Cost Model N=1 Ambiguity 🟡
- **Location:** `docs/reports/day08_reliability_economics.md` Table 2
- **Issue:** The N=1 row shows costs (Path A: $63.24M, Path B: $39.20M) that differ from the straightforward application of Eq. 2.2 (which would give $68.23M and $47.97M including refurbishment). The actual treatment is that N=1 represents the first flight with no refurbishment cost (booster is new), which is standard launch economics practice but was not documented.
- **Fix:** Added explanatory note before the "Key Insights" section.

### FIX-5: Engineering Notebook — Day 2 Heading Typo 🟡
- **Location:** `engineering_notebook.md` §2 heading
- **Error:** "First-Order S Sizing" → Fixed to "First-Order Sizing"

### FIX-6: Engineering Notebook — Day 2.4 S2 Mass Description 🟡
- **Location:** `engineering_notebook.md` §2.4
- **Issue:** "S2 Propellant / Dry Mass: 112,000 kg / 39,000 kg" was misleading — the 39,000 kg is the final stack mass (S2 structure+engine 5,500 + payload 20,000 + fairing 1,800 + interstage 2,500 + adapter 600 + avionics 1,600 + margin 7,000), not the structural dry mass alone.
- **Fix:** Expanded to show the full mass breakdown.

### FIX-7: Engineering Notebook — Day 3.5 Hover-Slam Physics 🟡
- **Location:** `engineering_notebook.md` §3.5
- **Issue:** "Minimum single-engine thrust (338 kN) exceeds the booster's near-empty weight" was incorrect — 338 kN (at SL, 40% throttle) is *below* the 410–441 kN weight. The statement conflated the design floor (40%) with the operational floor (50–57%).
- **Fix:** Rewrote to correctly describe the design vs. operational throttle floors and their relationship to hover. Added note about CR-D7-01.

### FIX-8: Engineering Notebook — Day 6.5 Open Risk Not Updated 🟡
- **Location:** `engineering_notebook.md` §6.5
- **Issue:** The open risk still said "high-fidelity 2-DOF descent simulation is required to verify the sufficiency of the 18,000 kg reserve" — but Day 7 already performed this simulation and proved the reserve insufficient.
- **Fix:** Added "Resolved on Day 7:..." annotation with the 34.5 t result.

### FIX-9: Day 7 Report — Path A GLOM Source Unexplained 🟢
- **Location:** `docs/reports/day07_trajectory_optimization.md` §7
- **Issue:** The 802 t GLOM was stated without noting that it comes from simulation interpolation (f=1.395 between f=1.35 at 790.5 t and f=1.40 at 816 t), not from the analytical n^0.8 structural mass scaling (which gives ~830 t).
- **Fix:** Added clarifying note explaining the simulation-based origin.

---

## Verified Correct (No Issues Found)

The following were explicitly verified as mathematically correct:

| Check | Result |
|---|---|
| Day 8 propellant cost: $0.5292/kg blended, Path A $0.37M, Path B $0.27M | ✅ Exact |
| Day 8 N=15 costs: Path A $37.65M (report $37.58M), Path B $24.45M (report $24.41M) | ✅ Within rounding |
| Day 8 capture energy: 90 kJ at 2 m/s, 562.5 kJ at 5 m/s (report 563 kJ) | ✅ Correct rounding |
| Day 2 reserve Δv: 1,028 m/s (SL) to 1,133 m/s (vac) → report says "1,030 m/s" and "1.03–1.13 km/s" | ✅ Correct |
| Day 7 S1 burn time: 391,000 / (305.5×9) = 142.2 s (report 142 s) | ✅ Correct |
| Day 7 S2 ideal Δv: 4,740 m/s with fairing jettison shortly after S2 ignition | ✅ Verified |
| Day 7 scaled family closure: f=1.40 at deficit −75 m/s, interpolated closure at f=1.395, GLOM=801,940 kg | ✅ Matches sim data |
| Day 6 hover throttle: 49–52% (SL) for 412–441 kN vehicle vs 845 kN max thrust | ✅ Correct |
| Mass budget closure: GLOM = 600,000 kg (assert in params.py) | ✅ Exact |
| Staging drop: 58,000 kg = struct + engines + HW + reserve | ✅ Exact |

---

## Suggestions for Future Improvement — Executed

All five actionable suggestions have been implemented (see below):

### SUGGEST-1: Cost Model Formula Consistency ✅ EXECUTED
The refurbishment cost is now formalized as a piecewise function (Eq. 2.5 in Day 8 report):
$$C_{\text{refurb}}(N) = \begin{cases} 0 & N = 1 \\ \$5.0\text{M} & N > 1 \end{cases}$$
All values in Table 2 have been recomputed for consistency (Path A at N=15: $37.65M, Path B at N=15: $24.45M; specific costs $1,883/kg and $2,038/kg respectively). All cross-references in Day 9, engineering notebook, and README have been updated.

### SUGGEST-2: Closed-Loop Guidance Memo ✅ EXECUTED
A comprehensive "Guidance Assumption Memo" has been added to Day 7 §6.3 (Ascent Monte-Carlo section). It documents: (i) the open-loop vs. closed-loop distinction, (ii) projected survival improvements under PEG-class guidance (Config A: 0.82→0.92–0.95; Config B convergence: 0.94→0.97–0.98), (iii) the structural g-exceedance is NOT a guidance problem, and (iv) full closed-loop MC verification is allocated as follow-on.

### SUGGEST-3: Day 2 Δv Requirement Correction ✅ EXECUTED
The engineering notebook Day 2 §2.2 now includes an explicit correction note documenting that the 11.0 km/s figure was an over-scoped planning estimate (~1,500 m/s above the physical need of ~9,500 m/s), referencing CR-D7-02.

### SUGGEST-4: Day 1–4 Deck Errors Documented ✅ EXECUTED
A new Appendix A has been added to the engineering notebook, tabulating all 10 known errors in the original Day 2–5 source PDFs (wrong dates, propellant mappings, Max-Q misreport, phantom orbital claims, landing count), with a note for the Day 10 competition deck to draw exclusively from the Day 7 repaired baseline.

### SUGGEST-5: FIGURE Placeholders in Day 6 Report ⏸ DEFERRED (as instructed)

### SUGGEST-6: Engine-Out Capability Analysis ✅ EXECUTED
A complete engine-out analysis has been added as engineering notebook §3.5, including: T/W table at 5 flight points (liftoff through MECO) for 9/8/7 engine configurations; gravity loss quantification (+152 m/s at liftoff EDO); payload penalty estimate (~4,000–4,500 kg); operational implications for Path A and Path B. Decision D3-3 added to the consolidated log. R-8 added to Day 9 traceability matrix. Day 9 reliability table enriched with EDO detail.

---

## Conclusion

The Days 1–7 materials are **engineering-sound at the systems level** — all major conclusions (two closure paths, 34.5 t reserve, hover-slam commitment, catch concept selection) remain valid. The fixes applied in this review corrected numerical precision issues (94.9% not 95.1%), one significant physics error in the Q&A defense (T/W calculation), and documentation inconsistencies from the Day 7 repair cycle. The suggestions above are improvements for polish and completeness, not corrections of fundamental errors.
