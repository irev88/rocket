# Day 2 — Rocket Fundamentals & First-Order Sizing
### AI Co-Design of a Reusable Rocket — Work Package 2 of 10
**Date:** 12 July 2026  
**Source:** Extracted from the central engineering notebook (`engineering_notebook.md`)

---

**Date**: 12 July 2026 (Day 2 of 10)  
**Deliverable**: First-Order Vehicle Sizing and $\Delta v$ Budget  
**Status**: Completed (Superseded in Day 7 Trajectory Repair)  

### 2.1 The Design Gate
Establish the Gross Lift-Off Mass (GLOM) and stage propellant/structural mass fractions required to close the mission using the Tsiolkovsky Rocket Equation.

### 2.2 Options Traded & Sizing Math
The team analyzed different mass ratios ($m_0/m_f$) and staging velocities using a target ideal $\Delta v$ budget of $11.0$ km/s, which included $9.3$ km/s orbital speed and $1.7$ km/s allocated to gravitational, drag, and steering losses. *(Day 7 correction CR-D7-02: the physical $\Delta v$ requirement for 500 km SSO is approximately 9,500 m/s — comprising 7,612 m/s circular velocity plus ~1,900 m/s realistic losses. The original 11.0 km/s figure was an un-optimized, conservative planning estimate that over-scoped the requirement by ~1,500 m/s.)*

*   **Sizing Model Formulation**:

$$
\Delta v_{\text{total}} = \Delta v_1 + \Delta v_2 = I_{sp,1} \, g_0 \ln\left(\frac{m_{0,1}}{m_{f,1}}\right) + I_{sp,2} \, g_0 \ln\left(\frac{m_{0,2}}{m_{f,2}}\right) \tag{2.1}
$$

*   Using an average $I_{sp}$ of $300$ s for S1 and $348$ s for S2, and assuming a Propellant Mass Fraction (PMF) of $0.85$ (reusable stage) and $0.90$ (expendable stage), the solver converged on a nominal **GLOM of 600,000 kg (600 tonnes)**, with a Stage 1 wet mass of $449,000$ kg and Stage 2 wet mass of $151,000$ kg.

### 2.3 LLM Copilot Insights
The Copilot highlighted the critical need for a **Recovery Propellant Reserve** to fund the entry and terminal burns of the first stage. This reserve must be carried through the entire S1 ascent as "dead mass," decreasing S1's effective mass ratio. The Copilot calculated that an **18,000 kg reserve** would provide approximately $1,030$ m/s of post-separation $\Delta v$ for a $40,000$ kg dry booster, which theoretically closes a downrange recovery corridor (entry burn $500–800$ m/s, landing burn $200–300$ m/s).

### 2.4 Decision and Rationale
*   **GLOM**: $600,000$ kg.
*   **S1 Propellant / Dry Mass**: $391,000$ kg / $40,000$ kg.
*   **S2 Propellant / Dry Mass**: $112,000$ kg propellant / $39,000$ kg final stack mass (comprising S2 structure+engine $5,500$ kg, payload $20,000$ kg, fairing $1,800$ kg, interstage $2,500$ kg, adapter $600$ kg, avionics $1,600$ kg, margin $7,000$ kg). The S2 structural dry mass alone is $5,500$ kg.
*   **Recovery Reserve**: $18,000$ kg, carried unburnt through ascent.
*   **Rationale**: Sizing at 600 t closes the mass budget while matching the thrust capabilities of nine Merlin-class engines, yielding a healthy lift-off thrust-to-weight ratio of $1.29$.

### 2.5 Open Risks Carried Forward
*   **Hobbyist S2 Sizing**: The first-order model lumped the fairing and second-stage structural margin together, requiring high-fidelity finite element and trajectory verification.

---


---

[← Day 1](../day01_mission_definition/report.md) | [Day 3 →](../day03_propulsion/report.md)

*Part of the AI Co-Design of a Reusable Rocket program. See the [central engineering notebook](../../engineering_notebook.md) for the full decision log.*
