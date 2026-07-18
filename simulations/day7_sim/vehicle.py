"""
vehicle.py — propulsion & aerodynamic models. Honest-physics rules:
 * Isp(h) interpolates linearly between SL and vacuum values by ambient
   pressure ratio  (1 - p/p0).  Isp can NEVER exceed the vacuum value.
 * Vacuum stage burns at constant vacuum Isp.
 * These two rules are the direct counter-measures to audit finding C-1.
"""
import math
import params as P
import atmosphere as AT

# ------------------------------------------------- dispersion hooks (Day 7 MC/DOE)
# Single-threaded per-sample perturbations.  Physics-honesty rules still hold:
# a positive Isp delta shifts BOTH sea-level and vacuum values (it models an
# engine that is uniformly better/worse than nominal).
DISP = dict(isp1_delta=0.0, isp2_delta=0.0, cd_scale=1.0)


def set_dispersion(isp1=0.0, isp2=0.0, cd=1.0):
    DISP.update(isp1_delta=isp1, isp2_delta=isp2, cd_scale=cd)


def clear_dispersion():
    set_dispersion(0.0, 0.0, 1.0)


# ---------------------------------------------------------------- propulsion
def s1_isp(h):
    """Stage-1 Isp(h): 282 s at SL pressure, 311 s in vacuum, never above 311."""
    pr = 1.0 - min(AT.pressure(h) / AT.P0, 1.0)
    return P.ISP1_SL + (P.ISP1_VAC - P.ISP1_SL) * pr + DISP["isp1_delta"]


def s1_thrust(h, throttle):
    """N, all 9 engines at given throttle (0.40–1.00)."""
    throttle = max(P.THROTTLE_MIN, min(P.THROTTLE_MAX, throttle))
    return throttle * P.N_ENG_S1 * P.MDOT1 * s1_isp(h) * P.G0


def s1_mdot(throttle):
    throttle = max(P.THROTTLE_MIN, min(P.THROTTLE_MAX, throttle))
    return throttle * P.N_ENG_S1 * P.MDOT1


def s2_thrust(h):
    """MVac runs vacuum-optimized; ignites >50 km where p/p0 < 1e-3."""
    return P.MDOT2 * (P.ISP2_VAC + DISP["isp2_delta"]) * P.G0


def s2_mdot():
    return P.MDOT2


# ---------------------------------------------------------------- aero
def cd(mach):
    table = P.CD_MACH
    if mach <= table[0][0]:
        return table[0][1]
    for (m0, c0), (m1, c1) in zip(table, table[1:]):
        if mach <= m1:
            f = (mach - m0) / (m1 - m0)
            return c0 + f * (c1 - c0)
    return table[-1][1]


def drag(v, h):
    """N, drag force magnitude opposing velocity."""
    if v <= 0.0:
        return 0.0
    m = AT.mach(v, h)
    return 0.5 * AT.rho(h) * v * v * cd(m) * P.A_REF * DISP["cd_scale"]


def dyn_pressure(v, h):
    return 0.5 * AT.rho(h) * v * v
