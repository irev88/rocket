# AI Co-Design of a Reusable Rocket — Project Status & Critical Review
**Prepared:** 16 July 2026 (Day 6 of 10) · Program window: 11–20 July 2026
**Scope of this document:** comprehension of the full project framework, audited status of all completed work (Documents: *Summer Program (5).pdf*, 4 presentation decks, *master data.pdf*), critical review of completed parts, and the forward plan for Days 6–10.

---

## 1. What the Project Is (Framework Comprehension)

A 10-day team project to **conceptually design a reusable launch vehicle with an LLM as engineering copilot**, graded on engineering *process* — requirements decomposition, multidisciplinary design optimization, trade-off analysis, uncertainty quantification, and engineering communication — rather than on "the best rocket."

**Support structure:** Prof. Xu (chief engineer); graduate mentors Yingjie & Jingjie (subsystem mentors); LLM copilot.

**The team's adopted mission (Day 1, locked):**

| Parameter | Value |
|---|---|
| Payload | **20,000 kg** to **Sun-Synchronous Orbit (SSO)** |
| Reusability | Reusable **first stage** (+~25% dry-mass penalty, ~20–25% payload penalty) |
| Cost | **< $30M/launch**, **10+ flights/year** |
| Propellant | **LOX/RP-1** both stages (chosen Day 1, confirmed Day 3) |

**The team's adopted vehicle (Days 2–5, converged):** a two-stage, Falcon-class kerolox launcher, **GLOM ≈ 600,000 kg**, 9× Merlin-class sea-level engines (Octaweb) + 1× Merlin-Vacuum-class upper-stage engine, aluminum-lithium FSW tanks, composite fairing/interstage — distinguished from Falcon 9 by a **hybrid ocean catch-compatible recovery** (catch ring + 4 catch lugs + replaceable wear shoes + minimal crush pads; vessel-side net/cable + hydraulic damping), inspired by the **Long March 10B debut of 10 July 2026** (verified real: first successful net-based orbital booster recovery, 7× YF-100K kerolox + 1× YF-219 methalox, ship *Linghangzhe*, ~6 min from separation to catch).

**Deliverables pattern observed:** each day = one report section (compiled in *Summer Program (5).pdf*, 91 pp) + one presentation deck (bilingual, mostly Chinese). *master data.pdf* = the OpenRocket trajectory export (1 table + 8 plots) backing Day 5.

---

## 2. Status Map — What Is Done, In Progress, Pending

| Day | Date | Theme (blueprint deliverable) | Status | Evidence |
|---|---|---|---|---|
| 1 | 11-Jul | Mission definition (mission requirements) | ✅ **Complete** | Report pp. 2–5; 4 core reqs; liquid-vs-solid verdict |
| 2 | 12-Jul | Rocket fundamentals (first-order sizing) | ✅ **Complete** | Report pp. 7–16; ~70-component functional grouping; Tsiolkovsky sizing; Δv budget; **Deck: Presentation (1).pdf** |
| 3 | 13-Jul | Propulsion system (engine selection) | ✅ **Complete** | Report pp. 18–26; kerolox selected; GG vs SC vs FFSC trade; Merlin 1D + MVac; **Deck: Day3-presentation.pdf** |
| 4 | 14-Jul | Mass budget & advanced materials (vehicle architecture) | ✅ **Complete** | Report pp. 29–76 (47 pp, w/ 36 refs); closed 600 t mass budget; hybrid catch architecture; materials map; **Deck: Day 4 (1).pdf** |
| 5 | 15-Jul | Aerodynamics & trajectory (flight profile) | ✅ **Complete (but see §4 — validation integrity issues)** | Report pp. 77–87; OpenRocket run; **Deck: Day 5 (1).pdf**; **Data: master data.pdf** |
| 6 | 16-Jul | Reusability strategy (recovery concept) | ✅ **FINALIZED (this review cycle)** — see `02_Day6_Reusability_Strategy_FINAL.md` | Report pp. 88–91 draft was truncated & contradicted Day 4 (boostback/legs); finalized version rebases everything on Day 1–4 + 16 cited sources; Day-5-derived states removed pending Day 7 repair |
| 7 | 17-Jul | AI-assisted optimization (design iteration) | ⬜ Pending | nothing yet |
| 8 | 18-Jul | Reliability & economics (cost and risk analysis) | ⬜ Pending | seeded data exists (Day 1 cost table; Day 4 mass/hardware split; Day 3 refurbishment drivers) |
| 9 | 19-Jul | Final system integration (technical review) | ⬜ Pending | nothing yet |
| 10 | 20-Jul | Design competition (final presentation) | ⬜ Pending | nothing yet; 4 decks exist as raw material |

**Blueprint outcomes checklist (§3 of Summer Program.pdf):** mission report ✅ · trajectory simulation ✅ (needs physics repair, §4) · mass budget ✅ · CAD sketches ⚠️ only text "Figure" placeholders in report · cost model ⬜ (Day 8) · **AI interaction logs / AI-generated engineering notebook ⚠️ NOT yet started — required by the blueprint; recommend starting immediately (decision log per day).**

---

## 3. What Passed Audit (Verified Consistent)

These checks were re-computed from the raw OpenRocket table in *master data.pdf*:

1. **Mass closure in the simulator exactly matches the Day 4 closed budget.** Stage drop at T+150→153 s = **58,000 kg** = first-stage dry (40,000) + recovery reserve (18,000) — the sim correctly carries the reserve *unburnt* through ascent, as stated in the Day 5 deck. Stage-2 burnable prop = 151,000 − 39,000 = **112,000 kg** exactly. Final mass 39,000 kg = S2 dry 5,500 + payload module 22,400 + interstage 2,500 + avionics 1,600 + margin 7,000. **Exact bookkeeping — a genuine strength.**
2. **Lift-off T/W = 1.29** (9×845 kN / 600 t) — matches report §6.3 and sits in the Day-3-deck optimal band 1.25–1.35.
3. **Closed mass budget sums exactly to 600,000 kg**; reported closure metrics reproduce (PMF 0.8683; λ = 3.33%; recovery fraction 3.92%).
4. **Recovery-reserve adequacy (downrange concept):** 18 t reserve on a 40 t dry booster at Isp ≈ 300 s ⇒ **~1.09 km/s available** vs ~0.8–1.35 km/s needed for entry burn + landing burn + settling — the downrange concept *closes*, tightly.
5. **LM 10B reference facts** in the Day 4 report (debut 10-Jul-2026, net/cable sea recovery, 7× YF-100K, 8,750 kN, 16 t LEO reusable) match external sources (Wikipedia, Ars Technica, 19FortyFive).
6. **Timeline realism for catch recovery:** from the sim's staging state, the booster coasts ~290 s to/from a ~180 km apogee ⇒ catch event ≈ **5–6 min after separation**, matching LM 10B's reported ~6 min.

---

## 4. Critical Review — Issues Found, Ranked

### 🔴 CRITICAL-1 — The Day 5 "validation" is not supported by the physics of the team's own data
Recomputed from *master data.pdf* (mass-balance identities, immune to thrust-curve details):

| Stage | Ideal Δv the sim kinematics imply | Mass ratio | **Effective Isp the sim must be using** | Declared engine Isp |
|---|---|---|---|---|
| Stage 1 (0→150 s) | 2,520 achieved + 1,201 gravity + 31 drag = **3,752 m/s** | ln(600/209)=1.054 | **≈ 363 s** | 282 s (SL) / 311 s (vac) |
| Stage 2 (153→543 s) | 5,080 achieved + 379 gravity = **5,459 m/s** | ln(151/39)=1.354 | **≈ 411 s** | 348 s (MVac) |

The simulated engines behave like **hydrolox-class engines (18–23% above kerolox physics)**. Cross-check: stage-2 mass flow (287 kg/s) exactly equals an MVac at full 981 kN — but the observed velocity gain (~5 m/s² near SECO on a ~40 t stack) is only ~1/5 of what 981 kN would produce. Mass consumption and velocity gain are mutually inconsistent in the export. **With the declared kerolox Isp values applied to the team's own mass model, total ideal Δv is ~7,540–7,840 m/s vs ~9,330 m/s needed for a 500 km SSO — a shortfall of ~1.5 km/s.** The Day 5 verdicts ("achieves 11.1 km/s ΔV, exceeding the 11.0 km/s requirement"; "all mission requirements satisfied") must be withdrawn and reworked — this is precisely the intended input to **Day 7 design iteration**.

### 🔴 CRITICAL-2 — The simulated trajectory does not close into orbit (≈150 m/s short)
Final exported state: 245.5 km, 7,610 m/s, vertical velocity 0. Local circular speed at 245.5 km is 7,762 m/s ⇒ vehicle is **152 m/s below circularization**; the resulting orbit's perigee altitude computes to **−248 km (suborbital)**. A ~150 m/s apogee circularization burn is required, but the sim burns the second stage to exactly dry mass (39,000 kg) — **zero propellant left**. The mission is also defined as 500 km SSO (Day 5 §2.3), while the sim ends at 245.5 km — orbit altitude is not even the mission orbit. Fixes: reserve ~200–250 kg of S2 prop for a circularization burn and/or loft the trajectory; re-run. (Note: the fairing, 1,800 kg, is also carried to orbit in the sim — jettisoning at ~100 km as the flight profile claims would partially offset this.)

### 🟠 MAJOR-3 — Day 5 Max-Q claims contradict the data; and the value exceeds the team's own stated limit
Report says "Max-Q ~25–30 kPa at ~12 km" and the verdict states "~28 kPa, well below structural limits." The data gives **q_max ≈ 40 kPa at T+60 s, 9.3 km altitude, Mach 1.24** (confirmed independently by the drag-force peak ≈ 230 kN at T+60–70 s, and a second local peak ~37.5 kPa at T+75 s — a double-peaked q-profile worth explaining). The report's own constraint band was 25–35 kPa ⇒ **the design as flown exceeds its stated structural limit.** Either re-run with a Max-Q throttle bucket (standard practice) or justify a 40 kPa structure. The current number in the verdict is simply misread from the tool.

### 🟠 MAJOR-4 — Day 6 draft recovery sequence contradicts the Day 4 architecture (and the reserve math)
The Day 6 draft (p. 90–91) writes a **three-burn profile starting with a "Boostback Burn"** and ends mid-sentence **"The landing legs deploy just before …"**. Both are wrong for this vehicle:
- **Boostback ⇒ RTLS.** The Day 4 baseline is **downrange ocean catch** (explicitly to *avoid* boostback). The 18 t reserve provides ~1.0–1.1 km/s; an RTLS boostback adds 300–500 m/s it cannot afford. The report even says so on p. 90 ("Site flexibility … drone ships for downrange recovery").
- **Landing legs are the documented fallback**, not the baseline (catch ring + wear shoes + crush pads). Day 5's flight profile also says "landing legs deploy" (p. 86) — same inconsistency carried over.
The draft also has a duplicated section number (two "1.3") and ends mid-sentence. → See companion file `02_Day6_Reusability_Strategy_DRAFT.md` for a corrected, ready-to-paste continuation.

### 🟠 MAJOR-5 — Staging/flight-profile numbers in the report text vs the data
- First-stage burn: report "**~158 s**" vs data MECO at **150 s**.
- Staging altitude: report "**~70/72 km**" vs data **78–82 km** (velocity 2.53 km/s — that part matches "~2.5–2.6").
- Booster coast apogee: flight profile says "**120–140 km**" vs ballistics from the sim's staging state ⇒ **~180–185 km**.
- Day 5 (p. 83) leaves the "Ascent Performance / Trajectory Losses" tables **empty** (figure placeholders never filled); §2.5 "where FT is thrust…" references an equation that did not render.
- Day 5 says stage re-enters "from ~2.6 km/s" slowed by drag "to ~300 m/s", but no descent simulation exists yet — OpenRocket ascent model does not cover the return leg. Day 6 must either bound the entry-burn state analytically (I provide the numbers) or declare it open.

### 🟡 MINOR-6 — Deck/report inconsistencies and factual slips
- **Day 4 deck mass table ≠ Day 4 report budget.** Deck: 420 t S1 prop / 75 t S2 / 24 t reserve (599,970). Report (superseding): 391 t / 112 t / 18 t (600,000). Update the deck before Day 10.
- **Day 3 deck propellant-example mapping errors:** "LOX/LH2 (Falcon 9)" — Falcon 9 is kerolox; "LOX/Methane (Long March 10B)" — LM 10B *booster* is kerolox (its *upper stage* is methalox, per the team's own Day 4 report). Correct mappings: Kerolox = Falcon 9 / Nebula-1 / LM-10B booster; Methalox = Starship / Zhuque-2; Hydrolox = Delta IV / Ariane 6.
- **Deck dates:** Day 2 deck titled "Day 2 7/11/2026" (Day 1's date) and **Day 4 deck "Day 4 13/7/2026" (Day 3's date)**.
- Day 6 draft cites SpaceX "over 400+ landings"; the team's own Day 4 report cites the **637th** landing (13-Jul-2026) — harmonize.
- Day 5 "finless configuration" — clarify "no *aerodynamic fins during ascent*; grid fins stowed and not modeled."
- Day 2 deck lists 3rd group as "Payload" containing avionics/recovery (report correctly names it "Avionics, Control & Recovery"). Deck slide 9/10 labeling should match report Group 3.
- LM 10B mass "760,000 kg" in Day 4 deck has no cited source (Wikipedia infobox lacks GLOM) — add citation or mark estimate.
- Report cover pages: Day 6 section has no deck yet (needed today, pattern implies).

### 🟡 MINOR-7 — Blueprint-process gaps to close before Day 10
- **AI interaction log / engineering notebook** (blueprint §3) — not started. Recommend a running `decision_log.md`: date, decision, options, rationale, sources, open risks. Cheap to do, high grading value.
- **CAD sketches** — the report contains only "Figure N:" captions with no images (Figures 1–5 in Day 4; two empty tables in Day 5). At minimum add schematic stack layout, catch-ring detail, recovery-sequence storyboard (can be vector schematics drawn programmatically).
- **Uncertainty quantification** (a stated core course goal) — currently only qualitative. Day 7 should carry simple Monte-Carlo/sensitivity on dry mass, Isp, reserve (seeded by report §6.5 code).

---

## 5. Quantitative Audit Table (for direct reuse in the report)

| Metric | Report claim | Recomputed from master data | Verdict |
|---|---|---|---|
| Max-Q | 25–30 kPa @ ~12 km; verdict "~28 kPa" | **~40 kPa @ T+60 s, 9.3 km, Mach 1.24** (2nd peak 37.5 kPa @ 75 s) | ❌ misreported; exceeds own 25–35 kPa band |
| Drag loss | 0.2–0.5 km/s assumed | ~**0.03 km/s** integrated (clean cylinder, no protuberances modeled) | ⚠️ optimistic; document assumption |
| Gravity loss | 1.0–1.5 km/s | ~**1.58 km/s** (S1 1.20 + S2 0.38) | ✅ within reason |
| Staging state | 72 km / 2.6 km/s / ~158 s burn | **82 km / 2.53 km/s / 150 s** (γ≈33°) | ⚠️ small mismatches |
| Final state | "orbital insertion, 7.62 km/s" | 245.5 km / 7.610 km/s, needs 7.762 ⇒ **−152 m/s, suborbital** | ❌ needs circularization burn |
| Effective S1 Isp | 282–311 s | **≈ 363 s implied** | ❌ OpenRocket motor not kerolox-physical |
| Effective S2 Isp | 348 s | **≈ 411 s implied** | ❌ same |
| Booster apogee | 120–140 km | **~180–185 km** (from staging state) | ❌ update profile |
| Recovery timeline | — | catch ≈ T+5–6 min after separation; vessel ≈ **550–650 km downrange** | ✅ new, feed Day 6 |
| Reserve adequacy | 18 t estimate | ~**1.0–1.1 km/s** available; OK downrange; **no boostback possible** | ✅ but bind text to it |

---

## 6. Day 6 (TODAY) — Completion Plan

**Deliverable due:** *Recovery concept* (report section + deck).

1. **Adopt the corrected Day 6 text** in `02_Day6_Reusability_Strategy_DRAFT.md` (ready to paste; fixes MAJOR-4; reuses LM 10B-verified facts; binds every burn to the 18 t / ~1.09 km/s reserve).
2. **Draw 3 schematics** (no CAD needed): (a) recovery timeline state-machine (separation→coast→entry burn→grid-fin descent→terminal burn→catch→safing), (b) catch-ring load-path diagram, (c) map-style downrange geometry (~600 km) with vessel window. 
3. **Produce the Day 6 deck** (~14 slides, outline included in the draft file) mirroring the bilingual style of prior decks; correct the date (16/7/2026).
4. **Close the loop explicitly to Day 4:** landing legs = documented fallback option; catch = baseline. One sentence in both places prevents a Day 9 review finding.
5. **Do NOT claim descent simulation exists** — present entry/terminal states as first-order analytic estimates flagged for Day 7 verification.

## 7. Days 7–10 Roadmap

- **Day 7 — AI-assisted optimization / design iteration.** The headline task is already defined by CRITICAL-1/2: repair trajectory physics (rebuild OpenRocket/custom integrator with true kerolox Isp 282/311/348), then run a documented trade: (a) GLOM growth to ~630–650 t, (b) payload 20→16–18 t, (c) methalox upper stage à la LM 10B (+~350 m/s), (d) Max-Q throttle bucket, (e) fairing-jettison modeling, (f) S2 circularization reserve. Pick one primary + one fallback; run Monte-Carlo on dry mass/Isp/reserve (report §6.5 dictionary is the seed). Deliverable: design iteration table before/after.
- **Day 8 — Reliability & economics.** Cost model: inherit Day 1 table (dev $2.0B, refurb $5M/flight, vehicle $40M first unit) → $/launch vs flight rate; booster amortization over 15 flights; recovery-vessel ops cost; compare legs-fallback refurb. Risk: FMEA table seeded by Day 4 §8.5 failure modes + engine-out (9-engine) + catch single-point failure analysis; reliability block diagram; reuse-passport inspection intervals.
- **Day 9 — System integration / technical review.** Traceability matrix: every Day 1 requirement → where closed (section, number, test); residual risks register; consistency pass across report + decks (all items in §4 above); red-team Q&A preparation.
- **Day 10 — Competition deck.** One narrative: requirement→architecture→verified performance→recovery innovation→economics. Fix the deck errors in MINOR-6 first. Lead with the LM 10B-validated catch concept and the sensor "reuse passport" — the team's most distinctive, defensible content.

## 8. Open Questions for Mentors (bring to Prof. Xu / Yingjie & Jingjie)

1. Acceptable to re-baseline orbit to "~245 km parking + circularization" wording, or must the sim demonstrate 500 km SSO directly? (drives Day 7 rerun scope)
2. Is the 25–35 kPa Max-Q band a hard constraint (→ throttle bucket) or may the structure be sized to 40 kPa (+mass)?
3. Catch-ring axial position "above CM at terminal descent" (Day 4 assumption, p. 48) — approve a simple pendulum-stability check for Day 7?
4. Recovery vessel ops cost ground rules for Day 8 (charter rate, sea-state availability 70–80%?) — provided or assumed?
5. CAD sketch expectations: schematic vector art acceptable, or is OpenRocket-layout screenshot sufficient?
