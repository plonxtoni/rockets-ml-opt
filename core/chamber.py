import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent)) 

from core.geometry import chamber_volume, burning_area, throat_area
from core.combustion import burn_rate
from core.nozzle import characteristic_velocity
from core.config import MotorConfig


def rhs(
    t, y, config: MotorConfig
):  # right hand side of the ode to be solved with scipy ivp
    # unpack state
    P_c, web = y

    # propellant characteristics
    R = config.propellant.R
    T_c = config.propellant.T_c
    rho = config.propellant.rho
    c_star = characteristic_velocity(config)

    # geometry calculations
    A_t = throat_area(config.nozzle)  # throat area
    A_b = burning_area(web, config.geom)  # grain burn area
    V_c = chamber_volume(web, config.geom)  # free chamber volume

    # combustion calculation
    r_b = burn_rate(P_c, config.propellant)  # burn rate (Saint Robert's law)

    dPcdt = ((R * T_c) / V_c) * (rho * A_b * r_b - (A_t * P_c) / c_star)
    dwebdt = r_b

    return [dPcdt, dwebdt]
