import numpy as np
from geometry import throat_area

def characteristic_velocity(propellant):
    R = propellant.R
    T_c = propellant.T_c
    gamma = propellant.gamma
    return np.sqrt((R*T_c)/gamma) * ((gamma+1)/2)**((gamma+1)/(2*(gamma-1)))

def mass_flow(P_c, propellant, nozzle):
    A_t = throat_area(nozzle)
    c = characteristic_velocity(propellant)
    return (P_c*A_t)/c

def thrust(P_c, P_amb, Propellant):
    gamma = propellant.gamma
    pressure_ratio_term = 1 - (P_amb / P_c) ** ((gamma - 1) / gamma)
    Cf = math.sqrt((2 * gamma**2 / (gamma - 1)) * (2 / (gamma + 1)) ** ((gamma + 1) / (gamma - 1)) * pressure_ratio_term)   # assuming perfectly expanded nozzle
    return = Cf * P_c * At