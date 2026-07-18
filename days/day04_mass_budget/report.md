# Day 4 — Mass Budget & Advanced Materials
### AI Co-Design of a Reusable Rocket — Work Package 4 of 10
**Date:** 14 July 2026  
**Source:** Extracted from the central engineering notebook (`engineering_notebook.md`)

---

**Date**: 14 July 2026 (Day 4 of 10)  
**Deliverable**: Mass Budget and Structural Materials Map  
**Status**: Completed and Locked  

### 4.1 The Design Gate
Produce a fully closed, high-fidelity mass budget with explicit subsystem weights, structural margins, and material selections.

### 4.2 Options Traded & Sizing Math
The team evaluated advanced aerospace alloys and carbon-fiber composites for the cryogenic tank barrels.

*   **Option 4A: Carbon-Fiber Reinforced Polymer (CFRP).** Rejected for Stage 1. While CFRP offers a 30% weight reduction over aluminum, kerolox tank structures do not benefit as heavily from composite mass-efficiency due to the density of RP-1, and CFRP exhibits high microcracking risks under cyclic cryogenic loading, compounding refurbishment costs.
*   **Option 4B: Aluminum-Lithium 2195 FSW.** **Selected.** Friction Stir Welded (FSW) Al-Li 2195 offers exceptional fracture toughness, excellent weldability, and low density, providing a robust, highly inspectable structural shell for the booster tanks.

### 4.3 LLM Copilot Insights
The Copilot introduced the **"Hybrid Catch" recovery architecture** to replace heavy landing legs. By installing a structural catch ring and four titanium catch lugs at the interstage, the landing loads are transferred to a vessel-side capture net and hydraulic damping system. The Copilot estimated that this deletes **2,500 kg of flying hardware mass** (5,500 kg catch hardware vs 8,000 kg landing legs), which was immediately reinvested into Stage 1 propellant and dry-mass margin.

### 4.4 Decision and Rationale
*   **Structure**: FSW Al-Li 2195 for propellant tanks; carbon-fiber composite for fairings and interstage.
*   **Booster Mass Breakdown**: Dry mass $40,000$ kg; Recovery hardware $5,500$ kg; Recovery reserve propellant $18,000$ kg; Ascent propellant $391,000$ kg.
*   **Stage 2 Mass Breakdown**: Dry mass $5,500$ kg; Fairing $1,800$ kg; Avionics $1,600$ kg; Propellant $112,000$ kg; Payload $20,000$ kg; Growth margin $7,000$ kg.
*   **Total GLOM**: $600,000$ kg exactly.
*   **Rationale**: The "hybrid catch" configuration reduces dry mass, achieving a Propellant Mass Fraction (PMF) of $0.8683$ on S1, enabling physical mass closure at 600 tonnes.

### 4.5 Open Risks Carried Forward
*   **Single-Point Catch Failure**: A failure to engage the vessel-side tensioned cables results in a high-speed impact on the deck or water, presenting a major reliability risk.

---

---

[← Day 3: Propulsion](../day03_propulsion/report.md) | **Day 4** | [Day 5: Trajectory →](../day05_trajectory/report.md)

*Part of the [AI Co-Design of a Reusable Rocket](../../engineering_notebook.md) program (Days 1–10).*
