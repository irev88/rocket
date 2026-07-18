# Day 3 — Propulsion System & Engine Selection
### AI Co-Design of a Reusable Rocket — Work Package 3 of 10
**Date:** 13 July 2026  
**Source:** Extracted from the central engineering notebook (`engineering_notebook.md`)

---

**Date**: 13 July 2026 (Day 3 of 10)  
**Deliverable**: Engine Selection and Propulsion Trade Study  
**Status**: Completed and Locked  

### 3.1 The Design Gate
Select the specific engine cycle and nozzle configurations for both stages, defining the thrust, specific impulse, and throttling limits.

### 3.2 Options Traded & Propulsion Trade Matrix
The team evaluated gas-generator (GG), staged-combustion (SC), and full-flow staged-combustion (FFSC) cycles for the kerolox propellant.

*   **Option 3A: Oxygen-Rich Staged Combustion (SC) — RD-180 Class.** Rejected. Offers high $I_{sp}$ ($\approx 311/338$ s) but carries extreme development costs, high dry weight, and complex refurbishment due to extreme turbine temperatures and pressures.
*   **Option 3B: Gas Generator (GG) — Merlin 1D Class.** **Selected.** Binds $845$ kN sea-level thrust and $914$ kN vacuum thrust with an $I_{sp}$ of $282$ s (SL) and $311$ s (vac). Offers exceptional thrust-to-weight ratio ($>150$), robust restart capability (4 restart cycles per mission), and a deep-throttle range down to 40% (essential for hover-slam).

### 3.3 LLM Copilot Insights
The Copilot warned that RP-1 thermal cracking (coking) at temperatures $> 260^{\circ}$C deposits carbon inside injector cooling channels, acting as the primary limiter for engine life. The Copilot suggested implementing an active nitrogen purge and oxygen-rich pre-burner purges post-cutoff to clear residual soot, targeting a **15-flight service life** per engine before a major rebuild.

### 3.4 Decision and Rationale
*   **Stage 1 Propulsion**: 9$\times$ Merlin 1D-class engines arranged in an Octaweb configuration.
*   **Stage 2 Propulsion**: 1$\times$ Merlin Vacuum (MVac)-class engine with an expanded nozzle area ratio ($165:1$), yielding a vacuum thrust of $981$ kN and a constant $I_{sp}$ of $348$ s.
*   **Rationale**: 9 engines provide a liftoff $T/W = 1.29$, within the optimal $1.25–1.35$ band, and offer engine-out capability during ascent. Throttling 3 engines for entry and a single engine for terminal hover-slam minimizes landing structural loads.

### 3.5 Engine-Out Capability Analysis

The 9-engine Octaweb configuration provides inherent engine-out operational capability (EDO). A first-order assessment was performed to quantify the performance impact:

**Thrust-to-Weight at Key Flight Points (1 Engine Out at T+0):**

| Flight Point | Vehicle Mass | 9-Engine T/W | 8-Engine T/W | 7-Engine T/W | Verdict |
|---|---|---|---|---|---|
| Liftoff | 600,000 kg | 1.29 | **1.15** | 1.01 | 8-eng: feasible; 7-eng: marginal |
| T+30 s | 521,800 kg | 1.49 | **1.32** | 1.16 | 8-eng: healthy |
| Max-Q (T+60 s) | 443,600 kg | 1.75 | **1.55** | 1.36 | 8-eng: comfortable |
| MECO (T+142 s) | 209,000 kg | 3.71 | **3.30** | 2.89 | 8-eng: no constraint |

**Performance Penalty:** A single engine failure at liftoff extends the S1 burn from 142 s to 160 s (reduced mass flow), increasing gravity losses by approximately **152 m/s** (from 1,217 to 1,369 m/s). This additional $\Delta v$ deficit must be compensated by the S2 stage, consuming extra propellant and reducing payload capability by approximately **4,000–4,500 kg** (first-order rocket equation estimate) or roughly **20–22%** of the nominal payload.

**Operational Implications:**
*   **Abort threshold:** At liftoff, loss of 2 engines ($T/W = 1.01$) leaves virtually no performance margin — flight termination would be required.
*   **Mission continuation:** Loss of 1 engine at any point after T+10 s (when $T/W > 1.5$ with 8 engines) permits safe mission continuation with significant payload reduction.
*   **Path A (20 t SSO):** The 2,088 m/s orbital deficit already consumes all available margin. An EDO event at liftoff would force mission abort or require drastic payload reduction to ~15–16 t SSO.
*   **Path B (12 t SSO):** EDO capability provides margin to reduce payload to ~8–10 t SSO and still achieve orbit.

### 3.6 Open Risks Carried Forward
*   **Hover-Slam Throttle Floor**: Minimum single-engine thrust ($338$ kN) exceeds the booster's near-empty weight ($\approx 410–440$ kN), preventing a true stable hover and forcing a committed "hover-slam" maneuver.

---

---

[← Day 2: Rocket Fundamentals](../day02_rocket_fundamentals/report.md) | **Day 3** | [Day 4: Mass Budget →](../day04_mass_budget/report.md)

*Part of the [AI Co-Design of a Reusable Rocket](../../engineering_notebook.md) program (Days 1–10).*
