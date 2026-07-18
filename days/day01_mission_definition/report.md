# Day 1 — Mission Definition & Requirement Decomposition
### AI Co-Design of a Reusable Rocket — Work Package 1 of 10
**Date:** 11 July 2026  
**Source:** Extracted from the central engineering notebook (`engineering_notebook.md`)

---

**Date**: 11 July 2026 (Day 1 of 10)  
**Deliverable**: Mission Requirements Document  
**Status**: Completed and Locked  

### 1.1 The Design Gate
Decompose the general prompt ("design a reusable launcher") into a set of four non-negotiable, citable mission requirements that govern the remainder of the 10-day MDO process.

### 1.2 Options Traded & Sensitivity Analysis
The trade revolved around the mission energy class (LEO vs GTO vs SSO) and propellant combinations (Liquid-vs-Solid, Kerolox-vs-Methalox-vs-Hydrolox) to lift a heavy cargo.

*   **Option 1A: Solid Booster Baseline.** Rejected. Solid rocket motors offer high thrust but lack restarting and deep-throttling capabilities, making them completely incompatible with propulsive vertical landing (VTVL).
*   **Option 1B: Liquid Hydrolox (LOX/LH2) Both Stages.** Rejected. Extremely low density of liquid hydrogen ($\approx 70$ kg/m$^3$) results in balloon-like tank volumes, expanding booster dry mass, aerodynamic drag, and manufacturing complexity, which violates the cost requirement.
*   **Option 1C: Liquid Kerolox (LOX/RP-1) Both Stages.** **Selected.** High density of RP-1 ($\approx 810$ kg/m$^3$) yields a highly compact, structurally efficient booster with excellent sea-level thrust-to-weight, utilizing mature, highly restartable gas-generator engine technology.

### 1.3 LLM Copilot Insights
The Copilot recommended setting a high-ambition commercial target: **20,000 kg (20 tonnes) to Sun-Synchronous Orbit (SSO)**, which sits in the lucrative megaconstellation and Earth-observation launch bracket. To offset the payload penalties of first-stage reusability, the Copilot suggested planning for a **15–20% payload penalty** and a **+25% first-stage dry-mass penalty** based on historical Falcon 9 operational data.

### 1.4 Decision and Rationale
*   **Payload**: $20,000$ kg to SSO (500 km altitude, $97.4^{\circ}$ inclination).
*   **Propellant**: LOX/RP-1 for both stages.
*   **Reusability**: First stage only (VTVL downrange ocean capture); second stage remains expendable due to high orbital-reentry thermal loads and mass constraints.
*   **Cost & Cadence**: $< \$30$M per launch, with a target cadence of $\ge 10$ flights/year.
*   **Rationale**: Kerolox offers the most compact first-stage tanks and the highest thrust-to-weight at lift-off, minimizing gross lift-off mass (GLOM). SSO downrange recovery exploits the booster's natural trajectory without requiring heavy return-to-launch-site (RTLS) propellant reserves.

### 1.5 Open Risks Carried Forward
*   **SSO Staging Energy**: Staging downrange requires a dedicated recovery ship and stable maritime operations.
*   **Coking and Sooting**: RP-1 combustion produces soot, which can degrade turbine blades and injectors, acting as the primary driver for refurbishment.

---

---

**Day 1** | [Day 2: Rocket Fundamentals →](../day02_rocket_fundamentals/report.md)

*Part of the [AI Co-Design of a Reusable Rocket](../../engineering_notebook.md) program (Days 1–10).*
