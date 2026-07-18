"""
params.py — Single source of truth for the Day-7 repaired simulation.
Every value carries a traceability comment to the Day 1–5 documents
(Summer Program (5).pdf / master data.pdf / Day3–Day5 presentations).
"""
import math

# ---------------------------------------------------------------- constants
G0   = 9.80665            # m/s^2  standard gravity
MU   = 3.986004418e14     # m^3/s^2 Earth gravitational parameter
R_E  = 6_371_000.0        # m      mean Earth radius (spherical model)

# ---------------------------------------------------------------- mission (Day 1 / Day 2)
PAYLOAD_T   = 20_000.0    # kg     Day 1 requirement
ORB_TGT_ALT = 500_000.0   # m      Day 2 §2.3: "500 km SSO", v_orb ≈ 7.6 km/s
DV_REQ      = 11_000.0    # m/s    Day 2 budget statement "≈11.0 km/s to SSO"
V_ORB_TGT   = math.sqrt(MU / (R_E + ORB_TGT_ALT))   # ≈7,612 m/s

# ---------------------------------------------------------------- masses (Day 4 closed budget, Day 5 §7)
M_PAYLOAD    = 20_000.0   # kg
M_ADAPTER    = 600.0      # kg
M_FAIRING    = 1_800.0    # kg
M_S2_DRY     = 5_500.0    # kg     (structure+engine, expendable)
M_S2_PROP    = 112_000.0  # kg
M_INTERSTAGE = 2_500.0    # kg
M_S1_STRUCT  = 27_000.0   # kg
M_S1_ENG     = 7_500.0    # kg     9 × ~833 kg as documented (Day 4)
M_REC_HW     = 5_500.0    # kg     recovery hardware (hybrid catch baseline)
M_S1_PROP    = 391_000.0  # kg     ascent propellant
M_S1_RESV    = 18_000.0   # kg     recovery reserve (NOT burned in ascent)
M_AVIONICS   = 1_600.0    # kg
M_MARGIN     = 7_000.0    # kg     dry margin

M_S1_DROP = M_S1_STRUCT + M_S1_ENG + M_REC_HW + M_S1_RESV          # 58,000 kg staging drop
GLOM = (M_PAYLOAD + M_ADAPTER + M_FAIRING + M_S2_DRY + M_S2_PROP + M_INTERSTAGE
        + M_S1_STRUCT + M_S1_ENG + M_REC_HW + M_S1_PROP + M_S1_RESV
        + M_AVIONICS + M_MARGIN)                                   # 600,000 kg
assert abs(GLOM - 600_000.0) < 1e-6, GLOM
assert abs(M_S1_DROP - 58_000.0) < 1e-6

# stack that remains after staging (fairing retained until early-S2 jettison)
M_S2_STACK = (M_PAYLOAD + M_ADAPTER + M_FAIRING + M_S2_DRY + M_S2_PROP
              + M_INTERSTAGE + M_AVIONICS + M_MARGIN)              # 151,000 kg
# final mass conventions
M_FINAL_FAIRING_KEPT = M_PAYLOAD + M_ADAPTER + M_FAIRING + M_S2_DRY + M_INTERSTAGE + M_AVIONICS + M_MARGIN  # 39,000 (Day 5 convention)
M_FINAL_FAIRING_DROP = M_FINAL_FAIRING_KEPT - M_FAIRING                                                   # 37,200 (physics convention)

# ---------------------------------------------------------------- geometry (Day 5 p.5–6)
DIAMETER   = 3.9                    # m
A_REF      = math.pi / 4 * DIAMETER**2
LENGTH     = 70.3                   # m

# ---------------------------------------------------------------- engines (Day 3)
# Merlin 1D-class first-stage engine.  Documented: SL 845 kN / vac 914 kN,
# Isp 282/311 s, throttle 40–100 %.  mdot calibrated to SL point; resulting
# vacuum thrust is 931.8 kN (+1.9 % vs. documented 914 kN — the four imported
# values are mutually inconsistent at the 2 % level; flagged in consistency
# register CR-D7-01).
N_ENG_S1   = 9
ISP1_SL    = 282.0
ISP1_VAC   = 311.0
THR1_SL    = 845_000.0              # N per engine at sea level
MDOT1      = THR1_SL / (ISP1_SL * G0)          # 305.5 kg/s per engine
THROTTLE_MIN = 0.40
THROTTLE_MAX = 1.00

# MVac-class second-stage engine.  Isp 348 s (vac).  mdot 287.0 kg/s matches
# master-data burn (112 t / 390 s) and gives 980.9 kN vac thrust.
N_ENG_S2   = 1
ISP2_VAC   = 348.0
THR2_VAC   = 981_000.0
MDOT2      = THR2_VAC / (ISP2_VAC * G0)        # 287.0 kg/s

# ---------------------------------------------------------------- aero model
# Cd(Mach) for a slender finless cylinder with tangent-ogive nose, base drag
# suppressed under power.  Engineering correlation level (no CFD).  Anchors:
# subsonic ~0.30, transonic peak 0.52 @ M1.1, supersonic decay to ~0.25.
CD_MACH = [(0.0, 0.30), (0.8, 0.33), (1.0, 0.44), (1.1, 0.52), (1.3, 0.46),
           (2.0, 0.38), (3.0, 0.32), (5.0, 0.27), (8.0, 0.24), (30.0, 0.22)]

# ---------------------------------------------------------------- flight program (S1)
T_KICK0  = 12.0          # s   start pitch-over (tower cleared ~150 m)
T_KICK1  = 24.0          # s   end pitch-over
PITCH_KICK = math.radians(12.0)   # total pitch imparted by T_KICK1 (tuned to master data)
# NOTE: tuned value — see validate.py G3 (match master data within 10 %)

# S2: ignite 3 s after MECO (Day 5 used 153 s), burn prograde (zero steering loss)
T_SEP_DELAY = 3.0

# fairing jettison when q < Q_FAIRING after S2 ignition (physics convention)
Q_FAIRING = 100.0        # Pa

# ---------------------------------------------------------------- limits
Q_STRUCT   = 35_000.0    # Pa  structural path constraint (Day 5 §2.4: 25–35 kPa)
G_AXIAL_MAX = 5.0        # g   Day 5 §2.4: <5–6 g

# ---------------------------------------------------------------- master data (Day 5 OpenRocket export) for validation overlay
MASTER = [
    # t(s), h(m), v(m/s), vv(m/s), Mach, m(kg), rho
    (0, 0, 0, 0, 0, 600000, 1.225),
    (10, 150, 32, 31, 0.09, 573933, 1.207),
    (20, 650, 68, 66, 0.2, 547867, 1.148),
    (30, 1500, 120, 116, 0.35, 521800, 1.058),
    (40, 3000, 190, 181, 0.55, 495733, 0.909),
    (50, 5500, 275, 255, 0.82, 469667, 0.697),
    (55, 7000, 335, 305, 1.0, 456633, 0.59),
    (60, 9300, 420, 375, 1.24, 443600, 0.458),
    (70, 15000, 610, 520, 1.8, 417533, 0.194),
    (75, 17000, 730, 610, 2.1, 404500, 0.141),
    (80, 20000, 860, 700, 2.45, 391467, 0.089),
    (90, 24000, 1150, 880, 3.25, 365400, 0.048),
    (100, 29000, 1450, 1040, 4.2, 339333, 0.0185),
    (110, 34000, 1750, 1180, 5.15, 313267, 0.0082),
    (120, 40000, 2030, 1300, 6.1, 287200, 0.00385),
    (130, 48000, 2260, 1410, 6.9, 261133, 0.00143),
    (140, 61000, 2410, 1460, 7.6, 235067, 0.00023),
    (150, 78000, 2520, 1400, 8.2, 209000, 0.000018),
    (153, 82000, 2530, 1380, 8.25, 151000, 0.00001),
    (180, 97000, 2890, 900, 9.3, 143246, 0.0000016),
    (360, 200000, 5460, 220, 17.7, 91554, 0.0000000011),
    (540, 245000, 7600, 2, 23.1, 39862, 0),
    (543, 245500, 7610, 0, 23.1, 39000, 0),
]
