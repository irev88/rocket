"""
sim.py — 3-DOF planar (downrange x, altitude h) ascent simulator over a
spherical Earth.  RK4 fixed-step integration, event-driven phases:

  S1 burn   : vertical rise -> pitch kick -> zero-AoA gravity turn,
              optional Max-Q throttle bucket, MECO at prop depletion
  staging   : instantaneous drop of M_S1_DROP, T_SEP_DELAY coast
  S2 burn   : prograde burn (zero steering loss), fairing jettison at q<Q_FAIRING
  coast     : optionally coast to apogee for orbit evaluation

Every step accumulates the loss decomposition integrals and the effective-Isp
diagnostic (audit counter-measures C-1 / M-3).
"""
import math
import params as P
import atmosphere as AT
import vehicle as V


def _gravity(x, h):
    """Spherical-earth gravity components in (x, h) frame."""
    r2 = x * x + (P.R_E + h) ** 2
    r = math.sqrt(r2)
    g = P.MU / r2
    return -g * x / r, -g * (P.R_E + h) / r


class Config:
    """Mission configuration — allows design-iteration sweeps without touching params.py."""
    def __init__(self, **kw):
        self.m_payload    = kw.get("m_payload",    P.M_PAYLOAD)
        self.m_adapter    = kw.get("m_adapter",    P.M_ADAPTER)
        self.m_fairing    = kw.get("m_fairing",    P.M_FAIRING)
        self.m_s2_dry     = kw.get("m_s2_dry",     P.M_S2_DRY)
        self.m_s2_prop    = kw.get("m_s2_prop",    P.M_S2_PROP)
        self.m_interstage = kw.get("m_interstage", P.M_INTERSTAGE)
        self.m_s1_dry     = kw.get("m_s1_dry",     P.M_S1_STRUCT + P.M_S1_ENG + P.M_REC_HW)  # 40,000
        self.m_s1_prop    = kw.get("m_s1_prop",    P.M_S1_PROP)
        self.m_s1_resv    = kw.get("m_s1_resv",    P.M_S1_RESV)
        self.m_avionics   = kw.get("m_avionics",   P.M_AVIONICS)
        self.m_margin     = kw.get("m_margin",     P.M_MARGIN)
        self.jettison_fairing = kw.get("jettison_fairing", True)
        self.q_limit      = kw.get("q_limit", None)          # Pa or None (no bucket)
        self.g_axial_max  = kw.get("g_axial_max", P.G_AXIAL_MAX)
        self.pitch_kick   = kw.get("pitch_kick", P.PITCH_KICK)
        self.t_kick0      = kw.get("t_kick0", P.T_KICK0)
        self.t_kick1      = kw.get("t_kick1", P.T_KICK1)
        self.dt           = kw.get("dt", 0.1)
        self.label        = kw.get("label", "config")
        # S2 pitch-biased guidance.  Modes:
        #  "schedule": theta = gamma + bias0*(1 - tb/hold)  (linear decay)
        #  "vcirc"   : bias = bias_max*(1 - v/v_circ(r)), floored at 0 —
        #              loft while slow, flatten toward orbital speed (PEG-like)
        self.s2_guidance  = kw.get("s2_guidance", "vcirc")
        self.s2_bias0     = kw.get("s2_bias0", math.radians(18.0))
        self.s2_bias_hold = kw.get("s2_bias_hold", 240.0)
        self.s2_bias_max  = kw.get("s2_bias_max", math.radians(30.0))
        self.n_eng_s2     = kw.get("n_eng_s2", 1)     # S2 engine-count study option
        self.n_eng_s1     = kw.get("n_eng_s1", P.N_ENG_S1)  # S1 engine-count option

    # ---- derived masses -------------------------------------------------
    @property
    def glom(self):
        return (self.m_payload + self.m_adapter + self.m_fairing + self.m_s2_dry
                + self.m_s2_prop + self.m_interstage + self.m_s1_dry
                + self.m_s1_prop + self.m_s1_resv + self.m_avionics + self.m_margin)

    @property
    def s1_meco_mass(self):
        return self.glom - self.m_s1_prop

    @property
    def s1_drop(self):
        return self.m_s1_dry + self.m_s1_resv

    @property
    def s2_stack(self):
        return self.s1_meco_mass - self.s1_drop

    @property
    def s2_final_mass(self):
        m = self.s2_stack - self.m_s2_prop
        if self.jettison_fairing:
            m -= self.m_fairing
        return m

    @property
    def tsiolkovsky_s1(self):
        # uses envelope-averaged Isp=296.5 s purely as a screening number
        return 296.5 * P.G0 * math.log(self.glom / self.s1_meco_mass)

    @property
    def tsiolkovsky_s2(self):
        m0 = self.s2_stack - (self.m_fairing if self.jettison_fairing else 0.0)
        return P.ISP2_VAC * P.G0 * math.log(m0 / self.s2_final_mass)


def run(cfg: Config, record_dt=1.0, verbose=False):
    """Integrate full ascent.  Returns dict with events, series, losses, orbit."""
    dt = cfg.dt
    # state
    t = 0.0
    x, h = 0.0, 0.0
    vx, vh = 0.0, 0.0
    m = cfg.glom
    throttle = 1.0
    phase = "S1"

    # event arrays
    rows = []          # (t, x, h, v, vv, mach, q, m, throttle, phase)
    events = {}
    # loss integrals
    I_thrust = I_grav = I_drag = I_steer = 0.0
    I_grav_s1 = I_drag_s1 = I_grav_s2 = I_drag_s2 = 0.0
    I_thrust_s1 = I_thrust_s2 = 0.0
    s1_burn_time = s2_burn_time = 0.0
    q_max, q_max_t, q_max_h, q_max_mach = 0.0, 0.0, 0.0, 0.0
    q_max_s1 = 0.0
    g_max = 0.0
    fairing_off = not cfg.jettison_fairing
    t_ign = None       # S2 ignition time (set at S2IGN event)

    def s1_prop_left():
        return m - cfg.s1_meco_mass

    def s2_prop_left():
        # prop remaining once staged (mass includes fairing until jettison)
        fairing_still_on = cfg.jettison_fairing and (not fairing_off)
        m_final_now = cfg.s2_final_mass + (cfg.m_fairing if fairing_still_on else 0.0)
        return m - m_final_now

    def thrust_vector(theta):
        return math.cos(theta), math.sin(theta)

    nxt = 0.0
    while True:
        v = math.hypot(vx, vh)
        vmag = max(v, 1e-9)
        ux, uh = vx / vmag, vh / vmag
        gamma = math.atan2(vh, max(vx, 1e-9)) if v > 1e-6 else math.pi / 2

        # ---------------- guidance: commanded direction ----------------
        if phase == "S1":
            if t < cfg.t_kick0:
                theta = math.pi / 2
            elif t < cfg.t_kick1:
                f = (t - cfg.t_kick0) / (cfg.t_kick1 - cfg.t_kick0)
                theta = math.pi / 2 - f * cfg.pitch_kick
                if v > 50:  # blend into gravity turn
                    theta = min(theta, gamma + cfg.pitch_kick * (1 - f))
            else:
                theta = gamma  # zero-AoA gravity turn
        elif phase in ("COAST_SEP",):
            theta = gamma
        else:  # S2 guidance
            if cfg.s2_guidance == "vcirc":
                r_loc = math.hypot(x, P.R_E + h)
                v_circ = math.sqrt(P.MU / r_loc)
                bias = cfg.s2_bias_max * max(0.0, 1.0 - v / v_circ)
            else:
                tb = t - t_ign
                bias = cfg.s2_bias0 * max(0.0, 1.0 - tb / cfg.s2_bias_hold)
            theta = gamma + bias
            # PEG-like end-game: never chase a falling velocity vector; hold
            # near-horizontal attitude so thrust stops adding radial-inward g.
            theta = max(theta, math.radians(-1.5))

        tx, th = thrust_vector(theta)

        # ---------------- throttle / bucket ------------------------------
        q = V.dyn_pressure(v, h)
        if phase == "S1" and cfg.q_limit is not None:
            if q > cfg.q_limit * 0.95:
                throttle = max(P.THROTTLE_MIN, throttle - (q / (cfg.q_limit * 0.95) - 1.0) * 2.0 * dt * 5.0)
            elif q < cfg.q_limit * 0.85:
                throttle = min(P.THROTTLE_MAX, throttle + 0.5 * dt)
        # axial-g limit (protect payload): cap throttle near MECO
        if phase == "S1" and v > 100:
            a_est = V.s1_thrust(h, throttle) * cfg.n_eng_s1 / P.N_ENG_S1 / m
            if a_est > cfg.g_axial_max * P.G0 + 9.8:
                throttle = max(P.THROTTLE_MIN, throttle - 1.0 * dt)
            elif a_est < cfg.g_axial_max * P.G0 + 6.0 and (cfg.q_limit is None or q < cfg.q_limit * 0.85):
                throttle = min(P.THROTTLE_MAX, throttle + 1.0 * dt)

        # ---------------- forces -----------------------------------------
        if phase == "S1" and s1_prop_left() > 0:
            T = V.s1_thrust(h, throttle)
        elif phase == "S2" and s2_prop_left() > 0:
            T = cfg.n_eng_s2 * V.s2_thrust(h)
        else:
            T = 0.0

        D = V.drag(vmag, h)
        gx, gh = _gravity(x, h)

        ax = (T * tx - D * ux) / m + gx
        ah = (T * th - D * uh) / m + gh

        # ---------------- RK4 step ---------------------------------------
        def deriv(st):
            _x, _h, _vx, _vh, _m = st
            _v = math.hypot(_vx, _vh)
            if _v > 1e-9:
                _ux, _uh = _vx / _v, _vh / _v
            else:
                _ux, _uh = 0.0, 1.0
            if phase == "S1" and (_m - cfg.s1_meco_mass) > 0:
                _T = V.s1_thrust(_h, throttle) * cfg.n_eng_s1 / P.N_ENG_S1
                _md = V.s1_mdot(throttle) * cfg.n_eng_s1 / P.N_ENG_S1
            elif phase == "S2":
                mf = cfg.s2_final_mass + (cfg.m_fairing if (cfg.jettison_fairing and not fairing_off) else 0.0)
                if (_m - mf) > 0:
                    _T = cfg.n_eng_s2 * V.s2_thrust(_h); _md = cfg.n_eng_s2 * V.s2_mdot()
                else:
                    _T = _md = 0.0
            else:
                _T = _md = 0.0
            _D = V.drag(_v, _h)
            _gx, _gh = _gravity(_x, _h)
            _ax = (_T * tx - _D * _ux) / _m + _gx
            _ah = (_T * th - _D * _uh) / _m + _gh
            return (_vx, _vh, _ax, _ah, -_md)

        st = (x, h, vx, vh, m)
        k1 = deriv(st)
        k2 = deriv(tuple(s + dt / 2 * k for s, k in zip(st, k1)))
        k3 = deriv(tuple(s + dt / 2 * k for s, k in zip(st, k2)))
        k4 = deriv(tuple(s + dt * k for s, k in zip(st, k3)))
        x, h, vx, vh, m = tuple(s + dt / 6 * (a + 2 * b + 2 * c + d)
                                for s, a, b, c, d in zip(st, k1, k2, k3, k4))
        t += dt

        # ---------------- integrals (projection method; ascent phases only) --
        if phase != "COAST":
            proj = (tx * ux + th * uh)
            I_thrust += (T / m) * proj * dt
            I_steer  += (T / m) * max(0.0, 1.0 - proj) * dt
            I_drag   += (D / m) * dt
            I_grav   += -(gx * ux + gh * uh) * dt
            if phase == "S1":
                I_thrust_s1 += (T / m) * proj * dt
                I_grav_s1 += -(gx * ux + gh * uh) * dt
                I_drag_s1 += (D / m) * dt
                s1_burn_time += dt if s1_prop_left() > 0 else 0.0
            elif phase == "S2":
                I_thrust_s2 += (T / m) * proj * dt
                I_grav_s2 += -(gx * ux + gh * uh) * dt
                I_drag_s2 += (D / m) * dt
                s2_burn_time += dt if s2_prop_left() > 0 else 0.0

        # ---------------- bookkeeping (ascent constraints only) -------------
        v = math.hypot(vx, vh)
        if phase != "COAST":
            q = V.dyn_pressure(v, h)
            if q > q_max:
                q_max, q_max_t, q_max_h = q, t, h
                q_max_mach = AT.mach(v, h)
            if phase == "S1" and q > q_max_s1:
                q_max_s1 = q
            a_sens = math.hypot(ax - gx, ah - gh)   # sensed (non-gravity) accel
            g_max = max(g_max, v > 1.0 and a_sens / P.G0 or 0.0)

        if t >= nxt:
            rows.append((t, x, h, v, vh, AT.mach(v, h) if h < 120_000 else 0.0,
                         q, m, throttle, phase))
            nxt += record_dt

        # ---------------- phase transitions -------------------------------
        if phase == "S1" and s1_prop_left() <= 0.5:
            events["MECO"] = dict(t=t, x=x, h=h, v=v, vh=vh, vx=vx,
                                  gamma=math.degrees(math.atan2(vh, max(vx, 1e-9))),
                                  m=m, mach=AT.mach(v, h) if h < 120_000 else 99.0)
            m -= cfg.s1_drop
            phase = "COAST_SEP"
            t_sep = t
        elif phase == "COAST_SEP" and t >= t_sep + P.T_SEP_DELAY:
            events["S2IGN"] = dict(t=t, x=x, h=h, v=v, m=m,
                                   gamma=math.degrees(math.atan2(vh, max(vx, 1e-9))))
            phase = "S2"
            t_ign = t
        elif phase == "S2" and (not fairing_off) and V.dyn_pressure(v, h) < P.Q_FAIRING and v > 200:
            m -= cfg.m_fairing
            fairing_off = True
            events["FAIRING"] = dict(t=t, h=h, m=m)
        elif phase == "S2" and s2_prop_left() <= 0.5:
            events["SECO"] = dict(t=t, x=x, h=h, v=v, vh=vh, vx=vx,
                                  gamma=math.degrees(math.atan2(vh, max(vx, 1e-9))), m=m)
            phase = "COAST"
        elif phase == "COAST":
            # integrate max 600 s or until apogee (vh through zero) below target
            if vh <= 0.0 and h > 50_000:
                events["APOGEE"] = dict(t=t, h=h, v=v)
                break
            if t - events["SECO"]["t"] > 900:
                break
        if h < -100 and "CRASH" not in events:
            events["CRASH"] = dict(t=t, x=x, h=h, v=v, phase=phase)
        if t > 1200 or h < -100:
            break

    # ---------------- orbit elements at SECO ----------------------------
    st = events.get("SECO")
    orbit = None
    if st:
        r = math.hypot(st["x"], P.R_E + st["h"])
        E = st["v"] ** 2 / 2 - P.MU / r
        a = -P.MU / (2 * E) if E < 0 else float("nan")
        L = (P.R_E + st["h"]) * st["vx"] - st["x"] * st["vh"]
        p = L * L / P.MU
        e = math.sqrt(max(1.0 - p / a, 0.0)) if not math.isnan(a) else float("nan")
        rp, ra = a * (1 - e), a * (1 + e)
        orbit = dict(a_km=(a) / 1000, e=e,
                     perigee_km=rp / 1000 - P.R_E / 1000,
                     apogee_km=ra / 1000 - P.R_E / 1000)

    # ---------------- shortfall to 500 x 500 km --------------------------
    deficit = float("nan")
    if orbit and not math.isnan(orbit["e"]):
        rt = P.R_E + P.ORB_TGT_ALT
        vc = math.sqrt(P.MU / rt)
        rp = orbit["perigee_km"] * 1000 + P.R_E
        ra = orbit["apogee_km"] * 1000 + P.R_E
        if rp >= rt - 1.0:
            deficit = 0.0
        else:
            # impulsive Hohmann accounting from current apsides (conservative-ish)
            a_now = (rp + ra) / 2
            v_apo = math.sqrt(P.MU * (2 / ra - 1 / a_now))
            a_tr = (ra + rt) / 2
            v_tr_apo = math.sqrt(P.MU * (2 / ra - 1 / a_tr))
            v_tr_per = math.sqrt(P.MU * (2 / rt - 1 / a_tr))
            deficit = (v_tr_apo - v_apo) + (vc - v_tr_per)

    return dict(cfg=cfg, rows=rows, events=events, orbit=orbit,
                deficit_to_500x500=deficit,
                q_max=q_max, q_max_t=q_max_t, q_max_h=q_max_h, q_max_mach=q_max_mach,
                q_max_s1=q_max_s1,
                g_max=g_max,
                losses=dict(I_thrust=I_thrust, I_thrust_s1=I_thrust_s1,
                            I_thrust_s2=I_thrust_s2, I_grav=I_grav,
                            I_drag=I_drag, I_steer=I_steer,
                            I_grav_s1=I_grav_s1, I_grav_s2=I_grav_s2,
                            I_drag_s1=I_drag_s1, I_drag_s2=I_drag_s2,
                            s1_burn_time=s1_burn_time, s2_burn_time=s2_burn_time),
                m_final=m)


def effective_avg_isp(res, stage):
    """Average Isp implied by integrated thrust work — audit counter-proof."""
    L = res["losses"]; cfg = res["cfg"]
    if stage == 1:
        num = L["I_thrust_s1"]
        m0, m1 = cfg.glom, cfg.s1_meco_mass
    else:
        num = L["I_thrust_s2"]
        m0 = cfg.s2_stack - (cfg.m_fairing if cfg.jettison_fairing else 0.0)
        m1 = cfg.s2_final_mass
    return num / (P.G0 * math.log(m0 / m1))
