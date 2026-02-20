from scipy.integrate import solve_ivp
from dataclasses import dataclass
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from core.config import MotorConfig
from core.chamber import rhs
from core.geometry import current_bates_grain_geometry, burning_area, burnout_web
from core.nozzle import thrust as compute_thrust, mass_flow, characteristic_velocity


@dataclass
class SimulationResult:
    t: np.ndarray
    P_c: np.ndarray
    web: np.ndarray
    r_i: np.ndarray
    L: np.ndarray
    A_b: np.ndarray
    thrust: np.ndarray
    m_dot: np.ndarray
    c_star: float
    total_impulse: float
    burned_mass: float
    burn_time: float
    converged: bool
    message: str


def simulate(t_span, y0, config: MotorConfig, P_amb=101325.0, **kwargs):
    web_max = burnout_web(config.geom)

    def ode(t, y):
        return rhs(t, y, config)

    def burnout(t, y):
        return web_max - y[1]

    burnout.terminal = True
    burnout.direction = -1

    sol = solve_ivp(ode, t_span, y0, events=burnout, dense_output=True, **kwargs)
    return make_result(sol, config, P_amb)


def make_result(sol, config: MotorConfig, P_amb=101325.0):
    t = sol.t
    P_c = sol.y[0]
    web = sol.y[1]

    r_i = np.array([current_bates_grain_geometry(w, config.geom)[0] for w in web])
    L = np.array([current_bates_grain_geometry(w, config.geom)[1] for w in web])
    A_b = np.array([burning_area(w, config.geom) for w in web])

    thrust_array = np.array([compute_thrust(p, P_amb, config) for p in P_c])
    m_dot_array = np.array([mass_flow(p, config) for p in P_c])

    return SimulationResult(
        t=t,
        P_c=P_c,
        web=web,
        r_i=r_i,
        L=L,
        A_b=A_b,
        thrust=thrust_array,
        m_dot=m_dot_array,
        c_star=characteristic_velocity(config),
        total_impulse=np.trapezoid(thrust_array, t),
        burned_mass=np.trapezoid(m_dot_array, t),
        burn_time=t[-1],
        converged=sol.status == 1,
        message=sol.message,
    )
