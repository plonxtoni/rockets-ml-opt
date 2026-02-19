import numpy as np

def current_bates_grain_geometry(web, geom):
    r_i = geom.r_i0 + web       # current inner radius (free volume), increasing due to inner surface burning
    L   = geom.L0 - 2 * web     # current length, decreasing due to ends burning
    return r_i, L

def burning_area(web, geom):
    if geom.grain_type == 'bates':
        r_i, L = current_bates_grain_geometry(web, geom)
        inner_surface = 2 * np.pi * r_i * L             # inner surface burning
        ends    = 2 * np.pi * (geom.r_o**2 - r_i**2)    # ends burning (annular surfaces)
        return inner_surface + ends
    else:
        NotImplementedError(f"Grain of type '{geom.grain_type}' not implemented")

def chamber_volume(web, geom, plenum=1e-3):
    if geom.grain_type == 'bates':
        r_i, L = current_geometry(web, geom)
        inner_free_volume = np.pi * r_i**2 * L          # inner free chamber volume
        ends_volume = 2 * np.pi * geom.r_o**2 * web     # free chamber volume at the ends
        return plenum + inner_free_volume + ends_volume
    else:
        NotImplementedError(f"Grain of type '{geom.grain_type}' not implemented")

def burnout_web(geom):
    radial_limit = geom.r_o - geom.r_i0     # due to decreasing grain thickness
    axial_limit  = geom.L0 / 2              # due to decreasing grain length
    return min(radial_limit, axial_limit)   # burnout occurs when either length or thickness is consumed

def throat_area(nozzle):
    return np.pi * nozzle.throat_radius**2