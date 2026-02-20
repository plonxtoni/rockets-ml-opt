import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from core.config import MotorConfig
from core.geometry import throat_area


def characteristic_velocity(config: MotorConfig):
    R = config.propellant.R
    T_c = config.propellant.T_c
    gamma = config.propellant.gamma
    c_star_theoretical = np.sqrt((R * T_c) / gamma) * ((gamma + 1) / 2) ** (
        (gamma + 1) / (2 * (gamma - 1))
    )
    return config.combustion.eta_cstar * c_star_theoretical


def mass_flow(P_c, config: MotorConfig):
    A_t = throat_area(config.nozzle)
    c_star = characteristic_velocity(config)
    return (P_c * A_t) / c_star


def thrust(P_c, P_amb, config: MotorConfig):
    gamma = config.propellant.gamma
    A_t = throat_area(config.nozzle)
    pressure_ratio_term = 1 - (P_amb / P_c) ** ((gamma - 1) / gamma)
    Cf_theoretical = np.sqrt(
        (2 * gamma**2 / (gamma - 1))
        * (2 / (gamma + 1)) ** ((gamma + 1) / (gamma - 1))
        * pressure_ratio_term
    )
    Cf = config.combustion.eta_cf * Cf_theoretical
    return Cf * P_c * A_t
