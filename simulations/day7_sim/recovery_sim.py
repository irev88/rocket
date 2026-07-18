"""
recovery_sim.py — S1 downrange-catch recovery chain simulator (Day 7 Arc B4).

Chain: separation state (from ascent sim) -> ballistic coast -> entry burn
(3 engines) -> unpowered atmosphere descent with grid-fin glide (L/D model)
-> terminal hover-slam (1 engine, throttle-map) -> capture interface.

Engineering-level models; every external figure is used ONLY as a validation
anchor (see DATA_SHEET / working notes), never as an input value.
"""
import math
import params as P
import atmosphere as AT
import vehicle as V

# ---------------------------------------------------------------- S1 recovery chain constants (own vehicle)
M_DRY_S1   = 40_000.0        # kg  struct+engines+recovery HW (Day 4)
M_RESV     = P.M_S1_RESV     # 18,000 kg recovery reserve
CD_A_STAGE = 18.0            # m^2  bluff base-first cylinder + fins (eng. estimate, swept in MC)
LD_GLIDE   = 1.3             # grid-fin glide L/D (own assumption; MC ±20%)
THR1_VAC   = P.MDOT1 * P.ISP1_VAC * P.G0   # 931.8 kN per engine (vac)
CAPTURE_H  = 15.0            # m   capture point above deck (net/cable height)
V_CAPTURE  = 2.0             # m/s vertical target at capture
LD_TAPER_H0 = 10_000.0       # m   grid fins hold full L/D down to this altitude...
LD_TAPER_H1 = 2_000.0        # m   ...then taper linearly to 0 (terminal verticalisation,
                             #     mirrors deployed-family practice: fins steer to a
                             #     vertical endgame before engine ignition)


def _grav(x, h):
    r2 = x * x + (P.R_E + h) ** 2
    r = math.sqrt(r2)
    g = P.MU / r2
    return -g * x / r, -g * (P.R_E + h) / r


def _drag(v, h, m_eta=1.0):
    return 0.5 * AT.rho(h) * v * v * CD_A_STAGE * m_eta


def integrate(state0, phases, dt=0.2, record=True):
    """Generic 2-DOF RK4 chain.
    state0: (t, x, h, vx, vh, m).  phases: list of dicts driving thrust/lift:
      kind='ballistic'|'entry_burn'|'glide'|'terminal'
    """
    t, x, h, vx, vh, m = state0
    rows = []
    log = {}
    for ph in phases:
        kind = ph["kind"]
        nxt = t
        while True:
            v = math.hypot(vx, vh)
            vm = max(v, 1e-9)
            ux, uh = vx / vm, vh / vm
            D = _drag(vm, h, ph.get("drag_scale", 1.0))
            # lift (grid-fin glide): perpendicular, "up-range" component chosen
            # to extend downrange: lift vector = rotate (-uh, ux) -> (+) x
            L = 0.0
            if kind in ("glide",):
                ld_nom = ph.get("LD", LD_GLIDE)
                if ph.get("ld_taper", True):
                    f = min(1.0, max(0.0, (h - LD_TAPER_H1) / (LD_TAPER_H0 - LD_TAPER_H1)))
                    ld_eff = ld_nom * f
                else:
                    ld_eff = ld_nom
                L = D * ld_eff
            # lift acts along (-uh? no): unit perp to v, pointing +x and +h mostly
            px_, ph_ = -uh, ux          # perp to velocity (left-normal)
            # ensure lift has +x component for downrange flight (vx>0)
            if px_ < 0:
                px_, ph_ = -px_, -ph_

            gx, gh = _grav(x, h)
            T, mdot, tl = 0.0, 0.0, ph.get("throttle", 0.0)

            if kind == "entry_burn":
                n_eng = ph.get("n_eng", 3); tl = ph.get("throttle", 0.60)
                ve = V.s1_isp(h) * P.G0
                # entry burn retrograde: thrust opposes velocity
                T = n_eng * tl * (P.MDOT1 * ve)
                Tx, Th_ = -ux * T, -uh * T
                mdot = n_eng * tl * P.MDOT1
            elif kind == "terminal":
                n_eng = ph.get("n_eng", 1); tl = ph.get("throttle", 0.70)
                ve = V.s1_isp(h) * P.G0
                T = n_eng * tl * (P.MDOT1 * ve)
                Tx, Th_ = 0.0, T          # vertical thrust (near-vertical endgame)
                mdot = n_eng * tl * P.MDOT1
            else:
                Tx = Th_ = 0.0
            if m - ph.get("m_floor", 0.0) <= mdot * dt:
                mdot = 0.0; T = 0.0; Tx = Th_ = 0.0   # reserve exhausted

            ax = (Tx - D * ux + L * px_) / m + gx
            ah = (Th_ - D * uh + L * ph_) / m + gh

            def dv(st):
                _x, _h, _vx, _vh, _m = st
                _v = math.hypot(_vx, _vh)
                if _v > 1e-9: _ux, _uh = _vx / _v, _vh / _v
                else: _ux, _uh = 0.0, -1.0
                return (_vx, _vh, ax, ah, -mdot)

            st = (x, h, vx, vh, m)
            k1 = dv(st); k2 = dv(tuple(s + dt/2*k for s, k in zip(st, k1)))
            k3 = dv(tuple(s + dt/2*k for s, k in zip(st, k2))); k4 = dv(tuple(s + dt*k for s, k in zip(st, k3)))
            x, h, vx, vh, m = tuple(s + dt/6*(a+2*b+2*c+d) for s, a, b, c, d in zip(st, k1, k2, k3, k4))
            t += dt
            if record and t >= nxt:
                rows.append((t, x, h, math.hypot(vx, vh), vh, m, kind))
                nxt = t + 2.0
            # phase exit conditions
            if kind == "ballistic" and ph.get("exit_h") is not None and h <= ph["exit_h"] and vh < 0:
                break
            if kind == "entry_burn" and ph.get("exit_h") is not None and h <= ph["exit_h"]:
                break
            if kind == "entry_burn" and ph.get("exit_v") is not None and math.hypot(vx, vh) <= ph["exit_v"]:
                break
            if kind == "glide" and h <= ph.get("exit_h", CAPTURE_H + 800):
                break
            if kind == "terminal" and (h <= CAPTURE_H or math.hypot(vx, vh) <= 0.5):
                break
            if h < -50 or t > 3600:
                break
        log[kind + "_exit"] = dict(t=t, x=x, h=h, v=math.hypot(vx, vh), vh=vh, m=m)
        if h < -50 or t > 3600:
            break
    return rows, log, (t, x, h, vx, vh, m)


def terminal_ignition_solution(v_ig, h_ig, m_ig, reserve_used, throttle_sched=((0.72,),),
                               v_target=V_CAPTURE, h_target=CAPTURE_H, dt=0.05):
    """Solve hover-slam: constant throttle, compute h_ign window for throttle band.
    Returns dict with ignition altitude window & prop use for target v<=2 at capture."""
    out = {}
    for tl in (0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00):
        m = m_ig; h = h_ig; v = v_ig; burned = 0.0
        ve = V.s1_isp(h) * P.G0
        T = tl * P.MDOT1 * ve
        mdot = tl * P.MDOT1
        # integrate vertical 1-D from ignition state (v downward negative conv: use descending positive)
        # v_ig given as descent speed (positive)
        while h > h_target and v > 0.0 and burned < (M_RESV - reserve_used):
            a_net = T / m - (P.MU / (P.R_E + h) ** 2) + 0.5 * AT.rho(h) * v * v * CD_A_STAGE / m
            v -= a_net * dt
            h -= v * dt
            m -= mdot * dt; burned += mdot * dt
            if v <= 0: break
        out[tl] = dict(h_final=h, v_final=v, burned=burned)
    return out


def solve_hover_slam_ignition(v_descent, h_start, m_start, reserve_available, v_target=V_CAPTURE,
                              tls=(0.45, 0.55, 0.60, 0.65, 0.70, 0.75, 0.85, 0.95)):
    """Find ignition altitude h_ign so that v(h_target) ≈ v_target at constant throttle,
    scanning throttle band — this is the V-2 ignition window."""
    window = []
    for tl in tls:
        # bisection on h_ign
        lo, hi = 200.0, h_start
        best = None
        for _ in range(26):
            mid = 0.5 * (lo + hi)
            r = _burn_from(v_descent, mid, m_start, tl)
            if r["v_final"] > v_target:
                lo = mid            # landed too fast -> ignite earlier (higher)
            else:
                hi = mid
            best = r
        window.append(dict(throttle=tl, h_ign=0.5*(lo+hi), **best))
    return window


def _burn_from(v0, h0, m0, tl, h_target=CAPTURE_H, v_floor=0.0, dt=0.05):
    m, h, v, burned = m0, h0, v0, 0.0
    ve = V.s1_isp(min(h0, 80_000.0)) * P.G0
    T = tl * P.MDOT1 * ve
    mdot = tl * P.MDOT1
    n = 0
    while h > h_target and v > v_floor and n < 20000:
        g = P.MU / (P.R_E + h) ** 2
        D = 0.5 * AT.rho(h) * v * v * CD_A_STAGE
        a = T / m - g + D / m
        v -= a * dt; h -= v * dt
        m -= mdot * dt; burned += mdot * dt
        n += 1
    return dict(v_final=v, h_final=h, burned=burned, t_burn=n*dt)
