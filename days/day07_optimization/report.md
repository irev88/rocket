# Day 7 — AI-Assisted Trajectory Optimization & Design Iteration
### AI Co-Design of a Reusable Rocket — Work Package 7 of 10
**Date:** 17 July 2026  
**Source:** Extracted from the central engineering notebook (`engineering_notebook.md`)

---

**Date**: 17 July 2026 (Day 7 of 10)  
**Deliverable**: Repaired Trajectory optimization, DOE, Monte-Carlo, and Iteration Log  
**Status**: Completed and Finalized  

### 7.1 The Design Gate
Optimize the ascent and descent trajectories, evaluate design robustness under dispersion, and iteratively re-baseline the vehicle configuration to achieve physical closure.

### 7.2 Results of Trajectory Optimization & Sensitivity
*   **Ascent Sensitivity (DOE)**: Running 1,200 Latin Hypercube samples revealed that pitch-kick start time ($t_{\text{kick},0}$) has the strongest positive correlation ($\rho = +0.48$) with orbital deficit, while S1 propellant loading ($m_{\text{prop,S1}}$) has the strongest negative correlation ($\rho = -0.42$).
*   **Ascent Optimization (Differential Evolution)**: Globally optimizing the guidance parameters yielded a tight performance ceiling, reducing the Config A deficit from $1,467$ m/s (grid) to **$1,427$ m/s** (global optimum). This proved that guidance-tuning alone cannot close the performance gap.
*   **Structural Overload (CR-D7-07)**: Config B (2$\times$ MVac) reaches a peak axial acceleration of **6.2–6.4 $g$** at SECO, structurally violating the 5.0 $g$ requirement due to its high thrust-to-weight ratio near burnout.

### 7.3 Recovery Solver & Fixed-Point Closure ($R^*$)
Integrating a 2-DOF descent chain simulator revealed that the **documented 18,000 kg propellant reserve is mathematically undersized by approximately 2$\times$**:
* An 18 t reserve restricts the entry burn to a hot Mach 2.89 corridor ($P_{\text{capture}} = 0.00\%$ under Monte-Carlo dispersions).
* Resolving Eq. 5.1 for a fixed-point closure $R^*$ shows that a **30–37 t reserve** is required.
* To survive real-world atmospheric and execution dispersions ($P \ge 0.95$ under Monte-Carlo), the reserve must be sized to **34.5–36.0 t** (recommended working point: **34.5 t** for a Mach 2.3 entry corridor, with the recovery ship positioned at **489 km downrange**).

### 7.4 Sizing Iteration Ladder (Paths to Closure)
The Copilot synthesized the repaired ascent and descent results into two viable, physically closed design paths for the Day 8 Reliability and Economics work package:

```
                  ======================================
                  | Day 7 Repaired Performance Baseline|
                  |     600 t GLOM / 20 t SSO Payload  |
                  |     Velocity Deficit: 2,088 m/s    |
                  ======================================
                                    |
                  __________________|__________________
                 |                                     |
    [Path A: Maintain 20 t SSO]            [Path B: Maintain 600 t GLOM]
                 |                                     |
  Upscale the entire launch vehicle      Restrict the payload to SSO:
  to achieve physical closure:           - 12.0 t Payload (2x MVac S2)
  - 802,000 kg GLOM (+34%)               - 6.6 t Payload (1x MVac S2)
  - 12x Merlin 1D (S1) / 4x MVac (S2)                  |
  - 34.5 t Recovery Propellant Reserve   Sizing: 34.5 t Recovery Reserve
                 |                       S2 Throttle required to mitigate
         CLOSED Sizing                         SECO acceleration overload (6.2 g)
                                                       |
                                                 CLOSED Sizing
```

*   **Path A (Payload-Driven Closure)**: Retains the 20 t SSO requirement by upscaling the vehicle to **802,000 kg GLOM** (+34% propellant scale), employing 12$\times$ M1D engines on S1 and 4$\times$ MVac engines on S2.
*   **Path B (GLOM-Driven Closure)**: Retains the 600,000 kg GLOM limit by restricting the reusable payload capability to **12,000 kg** (using 2$\times$ MVac on S2) or **6,600 kg** (using 1$\times$ MVac on S2).

### 7.5 Handoff to Day 8
These two closed design options—along with their quantified sensitivities, structural acceleration risks, and recovery reserve requirements—are formally delivered to Day 8 to perform the final cost-benefit optimization and fleet risk assessment.

---

---

[← Day 6: Reusability](../day06_reusability/report.md) | **Day 7** | [Day 8: Reliability Economics →](../day08_reliability_economics/report.md)

*Part of the [AI Co-Design of a Reusable Rocket](../../engineering_notebook.md) program (Days 1–10).*
