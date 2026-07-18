# Day 8 — Reliability and Economics
### AI Co-Design of a Reusable Rocket — Work Package 8 of 10
**Date:** 18 July 2026  
**Source:** Standalone report (not from the engineering notebook, which covers Days 1–7)

---

## Summary

This work package delivers the complete systems engineering, economic optimization, and reliability analysis for the reusable launch vehicle. Building on the two physically closed configurations from Day 7 (Path A: 802 t / 20 t SSO; Path B: 600 t / 12 t SSO), we:

1. **Quantitative Economics:** Built a parametric lifecycle cost model incorporating booster amortization (piecewise refurbishment: $0 for first flight, $5M thereafter), pressure-dependent propellant costs ($0.53/kg blended), maritime recovery operations ($1.5M/launch), and development amortization.
   - Path A achieves superior specific cost: **$1,883/kg** vs Path B's **$2,038/kg** (7.6% advantage)
   - Path B satisfies the absolute cost constraint: **$24.45M/launch** (vs $30M limit)

2. **Reliability Modeling:** Constructed a Reliability Block Diagram yielding:
   - Mission success: **$P_{\text{ascent}} = 98.2\%$**
   - Booster recovery success: **$P_{\text{recovery}} = 94.9\%$**
   - Attrition rate ≈5%, confirming the insurance premium factor in the cost model

3. **FMEA:** 10-line risk register with Risk Priority Numbers before and after mitigation. Top risk: terminal-burn center engine failure to relight (RPN 144 → 27 after redundant igniters and fail-safe trajectory bias).

4. **Over-Acceleration Mitigation (CR-D7-07):** Resolved the 6.2–6.4 $g$ SECO exceedance by implementing 40% throttle on S2 during the final 40 s of burn, reducing peak acceleration to 4.85 $g$ with only 120 kg payload penalty.

## Full Report

See **[full_report.md](full_report.md)** for the complete Day 8 report with all equations, tables, and analysis.

## Presentation

See **[presentation.pptx](presentation.pptx)** (9 slides, bilingual CN/EN).

---

[← Day 7: Optimization](../day07_optimization/report.md) | **Day 8** | [Day 9: System Integration →](../../docs/reports/day09_system_integration.md)

*Part of the [AI Co-Design of a Reusable Rocket](../../engineering_notebook.md) program (Days 1–10).*
