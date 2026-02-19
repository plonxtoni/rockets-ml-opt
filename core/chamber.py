from geometry import chamber_volume, burning_area, throat_area
from combustion import burn_rate
from nozzle import characteristic_velocity

def rhs(t, y, propellant, geom, nozzle):      # right hand side of the ode to be solved with scipy ivp
    # propellant characteristics 
    R = propellant.R
    T_c = propellant.T_c
    rho = propellant.rho

    # geometry calculations
    A_t = throat_area(nozzle)           # throat area
    A_b = burning_area(web, geom)       # grain burn area
    V_c = chamber_volume(web, geom)     # free chamber volume
    
    # combustion calculation
    r_b = burn_rate(P_c, propellant)    # burn rate (Saint Robert's law)
    
    # unpack state
    P_c, web = y
    
    dwebdt = burn_rate(P_c, propellant)
    dPcdt = ((R*T_c)/V_c) * (rho*A_b*r_b - (A_t/characteristic_velocity(propellant)*P_c))

    return [dPcdt, dwebdt]