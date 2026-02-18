def mass_flow(P, propellant, nozzle):
    a_t = np.pi * nozzle.throat_radius**2
    γ = propellant.gamma
    return a_t * P * np.sqrt(γ/(propellant.R*propellant*Tc)) * (2/(γ + 1)) ** ((γ+1)/(2*(γ-1)))

def thrust(P, Pamb, Propellant):
    γ = propellant.gamma
    pressure_ratio_term = 1 - (Pamb / P) ** ((γ - 1) / γ)
    Cf = math.sqrt((2 * γ**2 / (γ - 1)) * (2 / (γ + 1)) ** ((γ + 1) / (γ - 1)) * pressure_ratio_term)
    return = Cf * P * At
