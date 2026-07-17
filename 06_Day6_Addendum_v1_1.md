# Day 6 (Reusability Strategy / Recovery Concept) — Addendum v1.1

**Issued**: 2026-07-17 (Day 7) · **Scope**: corrections to `02_Day6_Reusability_Strategy_FINAL.md` and `Day6_可重复使用策略_回收概念.pptx` following the Day 5/Day 7 model repair.
**Rule applied**: finalized documents are not silently edited → the report stands with this addendum; the slide deck was regenerated as **v1.1** (source: `day6_assets/build_day6_ppt.py`).

---

## 1. What changes (Day 6 errata)

| # | Location (report / slide) | Was | Now (v1.1) | Driver |
|---|---|---|---|---|
| E-1 | Report §5 / Slide 9 (phase table) | separation "T+150–165 s, ≈65–80 km, 2.0–2.3 km/s (anchor estimate)" | **T+142 s, 66.5 km, 1,892 m/s, γ≈41°, Mach 5.7, downrange 51 km (Day 7 model)** | honest ascent |
| E-2 | Slide 9 | apogee "≈130–200 km" | **≈135 km** (from v⊥≈1.23 km/s at separation) | E-1 |
| E-3 | Slide 9 / report §5 bullet | "all values are anchor estimates; V-1 open" | anchor text retained for F9/LM-10B; **own-vehicle line replaced by model values**; remaining open item narrowed to entry/terminal segments (V-2/V-4) | V-1 closed |
| E-4 | Slide 14 (V&V handoff bar) | "V-1 分离状态复算 ⇒ Day 7" | **"V-1 — initial values delivered by Day 7 model"** | V-1 closed |
| E-5 | Slide 15 title / verdict | "闭合且被验证" | "**回收侧**闭合且被验证" (recovery-side closure) + Day-7 flag bar | honesty split |
| E-6 | Slide 15 bottom bar | plain handoff | adds: **600 t documented stack misses 500×500 by 2,088 m/s; 600 t reusable capability ≈6.6 t; closure = architecture re-scale ≈802 t or payload relief ⇒ Day 8 decision** | repaired mission accounting |
| E-7 | Report figure/table references to Day 5 trajectory ("[FIGURE N]" placeholders) | Day 5 plots intended | use Day 7 `results/fig1–fig6` instead | retired data |

## 2. What does NOT change (verified unaffected)

1. **Method selection**: hybrid ocean net/cable catch; downrange mode (RTLS excluded).
2. **Recovery mass & propellant closure**: capture mass 42–45 t; Δv_avail = 1.03–1.13 km/s vs 0.8–1.2 km/s need; legged fallback numbers; hybrid savings (−2.5 t HW / −6 t reserve).
3. **Terminal physics**: hover-slam (49–52% throttle uncertainty → no hover); fail-safe trajectory; capture energy 90→563 kJ; interface targets (≤2 m/s, ≤5 m, ≤3°, ≤1°/s); load path & wear-boot concept.
4. **Economics & external anchors** (all 23 references + LM-10B/F5/F7 entries).
5. **Ship position ≈430 km downrange** remains defensible: honest separation (γ 41°, vx ≈1.43 km/s) ⇒ apex ≈135 km at ~230 km downrange + hypersonic glide extension; flagged as **sensitivity −8 % on separation velocity** for the V-4 corridor re-check.

## 3. Consistency Register — new entries (append to report §9)

| ID | Item | Status |
|---|---|---|
| CR-D7-01 | Merlin 1D documented set inconsistent: 845 kN SL + Isp 282/311 s ⇒ vac thrust 932 kN ≠ documented 914 kN (+1.9 %) | kept as documented (mdot calibrated to SL); flag to Day 3 correction on next revision |
| CR-D7-02 | Day-2 requirement "11.0 km/s to SSO" vs physical need ≈ 7,612 orbital + ~1,900 losses ⇒ **inflated requirement** ≈ +1,100–1,400 m/s | recommend requirement revision at Day 8 (affects all Δv bookkeeping) |
| CR-D7-03 | Day-2/5 claimed capability "11.1 km/s" vs honest ideal **7,875 m/s** | resolved: claim retired with Day 5 model |
| CR-D7-04 | Day-1 requirement 20 t SSO vs honest reusable capability **≈6.6 t at 600 t** (12 t with 2nd MVac) | **open decision → Day 8**: re-scale (GLOM ≈802 t) / payload relief / expendable sub-fleet (14 t) |
| CR-D7-05 | Fairing: retired model carried fairing to orbit (39.0 t final); physics convention jettisons at S2 ignition (37.2 t) | adopt jettison (~+100 m/s); mass finals reconciled both conventions |
| CR-D7-06 | Day-6 V-1 anchor band (2.0–2.3 km/s) vs honest 1,892 m/s | V-1 updated (E-1); recovery quotas re-check at chosen architecture point (Day 8) |

## 4. Version ledger

| Date | Artifact | Action |
|---|---|---|
| 2026-07-16 | Day 6 report FINAL, deck v1.0, SVG×4, image prompts | issued |
| 2026-07-17 | Deck **v1.1** | E-1…E-6 applied; layout audit clean (15 slides) |
| 2026-07-17 | `05_Day5_Repair_and_Completion.md`, `day7_sim/` + `DATA_SHEET.md` | Day 5 retired & completed; model + datasets issued |
