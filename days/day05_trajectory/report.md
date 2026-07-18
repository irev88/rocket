# Day 5 — Aerodynamics & Trajectory (Retired & Repaired)
### AI Co-Design of a Reusable Rocket — Work Package 5 of 10
**Date:** 15 July 2026  
**Source:** Extracted from the central engineering notebook (`engineering_notebook.md`)

---

**Date**: 15 July 2026 (Day 5 of 10)  
**Deliverable**: Trajectory Simulation and Flight Profile  
**Status**: **RETIRED AND REPAIRED** (Physics-Invalid Baseline)  

### 5.1 The Design Gate
Simulate the ascent flight profile and verify that the 600 t vehicle achieves orbital insertion at 500 km SSO with a 20 t payload.

### 5.2 The Trajectory Defect (Audit & Discovery)
The initial OpenRocket trajectory simulation (which claimed successful insertion with $+100$ m/s margin) was audited by the Copilot and found to violate basic physics:
- **Implied $I_{sp}$ Inflation (C-1)**: To achieve the reported velocities, the OpenRocket model utilized a constant high thrust that implied an impossible average S1 $I_{sp}$ of **$364$ s** (vacuum limit is 311 s) and S2 $I_{sp}$ of **$427$ s** (vacuum limit is 348 s). This "phantom energy" amounted to a $+1.5$ km/s over-performance.
- **Suborbital Final State (C-2)**: The reported final state (245 km, $7,610$ m/s, $\gamma = 0^{\circ}$) resulted in a highly suborbital trajectory with a perigee of **$-248$ km**, meaning the vehicle would re-enter the atmosphere immediately rather than completing an orbit.
- **Max-Q Misread (M-3)**: The report claimed Max-Q of $28$ kPa @ 12 km, but the raw master data table showed a peak of **$40.4$ kPa @ 9.3 km**, exceeding the structural design limit of $35$ kPa.

### 5.3 LLM Copilot Insights & Model Repair
The Copilot recommended a complete halt to the trajectory compilation and spearheaded a rigorous **model repair**. Operating in `simulations/day7_sim/`, the Copilot rebuilt a 3-DOF planar numerical integrator from first physical principles, incorporating the US Standard Atmosphere 1976 and pressure-dependent $I_{sp}$ bounds. This repaired model successfully passed all 8 acceptance gates (`results/gate.json`), proving energy conservation and providing honest physical baselines.

### 5.4 Decision and Rationale
*   **Staging Point**: Corrected to $t+142$ s, $66.5$ km altitude, $1,892$ m/s velocity ($\text{Mach } 5.7$), $\gamma = 40.7^{\circ}$, and $51$ km downrange.
*   **Orbital Deficit**: Re-simulating the documented 600 t vehicle with honest physics reveals an actual velocity deficit of **2,088 m/s** to reach orbit.
*   **Action**: Formally retire the Day 5 trajectory table and master data plots, carrying the true $2,088$ m/s deficit into the Day 7 optimization cycle.

---

---

[← Day 4: Mass Budget](../day04_mass_budget/report.md) | **Day 5** | [Day 6: Reusability →](../day06_reusability/report.md)

*Part of the [AI Co-Design of a Reusable Rocket](../../engineering_notebook.md) program (Days 1–10).*
