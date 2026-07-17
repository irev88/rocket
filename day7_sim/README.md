# day7_sim — Day 7 repaired ascent model & study suite

Replaces the retired Day 5 OpenRocket model. All Day 1–4 documented parameters are used verbatim (`params.py` asserts GLOM = 600,000 kg and staging drop = 58,000 kg exactly).

## Method (short)

- 3-DOF planar (downrange x, altitude h), spherical-Earth gravity, RK4 @ dt 0.1 s
- USSA76 exponential-layer atmosphere (validated against standard values)
- Honesty rules: Isp(h) = 282 + 29·(1 − p/p0) s with **hard ceiling at vacuum value**; S2 = 348 s constant; q and sensed-g tracked every step; fairing jettisoned at q < 100 Pa
- S1 flight program: vertical rise → pitch kick (12–30 s, 3.5°) → zero-AoA gravity turn; optional Max-Q throttle bucket + axial-g (5 g) cap
- S2: PEG-like loft-bias schedule + end-game attitude floor; per-point guidance tuning grid emulates trajectory optimization (full collocation/PEG = follow-on B3)
- Orbit: state-vector elements at SECO; deficit = impulsive Hohmann accounting to 500×500 km

## Run

```bash
python3 studies.py    # S0–S7 suites  -> results/*.json   (~3 min)
python3 validate.py   # 8-gate audit   -> results/gate.json (must be 8/8 PASS)
python3 plots.py      # fig1–fig6      -> results/fig*.png
# --- Arc B (DOE / optimization / Monte-Carlo / recovery) ---
python3 run_recovery.py  # R1–R5 recovery chain & reserve closure      (~2 min)
python3 doe.py           # B2 LHS sensitivity + B3 diff-evolution       (~25 min)
python3 mc.py            # B5 Monte-Carlo ascent + recovery            (~3 min)
python3 plots2.py        # fig7–fig13                                   (<1 min)
```

## Results map

- **Baseline/audit**: `S0_baseline.json`, `S0_audit_implied_isp.json` (old-data implied Isp 364/427 s)
- **Studies**: `S1_bucket` (Max-Q), `S2_split` (T/W boundary), `S3_payload`, `S4_expendable`, `S5_growth_1mvac` (barrier), `S6*` (2nd-MVac & scaled family), `S6d_closure_estimate` (GLOM≈802 t), `S7_closure_points` (refined closure payloads), `ALL_results.json`
- **Recovery (B4)**: `R1_chain` (profile, γ consistent), `R2_entry_sizing` (corridor vs reserve, dry-mass floor), `R3_terminal_window` (V-2), `R4_closure` (reserve fixed point R* 30–37 t), `R5_ship` (V-4 ≈489 km)
- **Sensitivity/optimization (B2/B3)**: `S8_sensitivity.json` + `S8_samples_{A,B}.json` (600 LHS/config), `S9_optimized.json` (DE ceiling: A 1,427 / B 871 m/s; B_gconstrained: g-exceedance structural)
- **Monte-Carlo (B5)**: `S10_mc_ascent.json` (+ samples, conditioned stats), `S11_mc_recovery.json` (+ samples: P0 P(close)=0.0, P1 P=0.45)
- **Figures**: `fig1_profile` … `fig6_ladder`, `fig7_recovery_profile` … `fig13_mc_recovery` (plots2.py)
- **Key numbers for documents**: `DATA_SHEET.md` (single citable source of truth)

## Known limitations

Guidance is a tuned family (deficits are tight upper bounds — DE gains ≤40 m/s); 1×-MVac endgame arc-sag is a guidance artifact; no Earth-rotation credit; engineering-correlation aero only; recovery frame spherical-gravity (≈3% energy-consistent); MC uses open-loop guidance (survival pessimistic). See `DATA_SHEET.md` §5 & §7.3 for the full honesty list.
