"""
atmosphere.py — 1976 US Standard Atmosphere, exponential-layer approximation.
Valid 0–1000 km for engineering ascent work (drag becomes negligible >120 km).
Layers: (base_altitude_m, base_rho_kg/m3, scale_height_m, base_T_K)
"""
import math

# (h_base, rho_base, H, T_base)  — USSA76 values at layer bases
_LAYERS = [
    (0,      1.2250,     8_434.0, 288.15),
    (11_000, 0.36392,    6_341.0, 216.65),
    (20_000, 0.08803,    6_382.0, 216.65),
    (32_000, 0.01322,    6_995.0, 228.65),
    (47_000, 0.00143,    7_077.0, 270.65),
    (51_000, 0.00086,    6_959.0, 270.65),
    (71_000, 0.000064,   6_555.0, 214.65),
    (84_852, 0.00000696, 7_000.0, 186.95),
    (100_000, 5.6e-7,    8_400.0, 195.08),
    (120_000, 2.2e-8,   12_000.0, 360.0),
    (200_000, 2.5e-10,  40_000.0, 1_000.0),
]

GAMMA_AIR = 1.4
R_AIR     = 287.05
P0        = 101_325.0


def _layer(h):
    for i in range(len(_LAYERS) - 1):
        if h < _LAYERS[i + 1][0]:
            return _LAYERS[i]
    return _LAYERS[-1]


def rho(h):
    """Density kg/m^3."""
    if h < 0:
        h = 0.0
    hb, rhob, H, _ = _layer(h)
    return rhob * math.exp(-(h - hb) / H)


def temperature(h):
    hb, _, _, Tb = _layer(h)
    return Tb


def pressure(h):
    """Hydrostatic-consistent pressure via rho * R * T (engineering accuracy)."""
    return rho(h) * R_AIR * temperature(h)


def sound_speed(h):
    return math.sqrt(GAMMA_AIR * R_AIR * temperature(h))


def mach(v, h):
    return v / sound_speed(h)


if __name__ == "__main__":
    # sanity table vs USSA76 standard values
    checks = [(0, 1.225), (11_000, 0.3639), (20_000, 0.0880), (50_000, 1.027e-3),
              (60_000, 3.06e-4), (80_000, 1.85e-5), (100_000, 5.6e-7)]
    for h, ref in checks:
        got = rho(h)
        print(f"h={h:>7.0f} m  rho={got:.4e}  ref≈{ref:.4e}  ratio={got/ref:.3f}")
