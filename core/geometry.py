import numpy as np

def burning_area(web, geom):
    if geom.grain_type=='bates': #simple cylindrical grain
        r_i = geom.r_o - web
        return 2*np.pi*r_i*geom.L
    #TODO: implement star geometry for comparison experiments

def chamber_volume(web, geom, plenum=1e-3):
    if geom.grain_type=='bates': #simple cylindrical grain
        r_i = geom.r_o - web
        return plenum + np.pi*geom.r_i**2*geom.L

def dVdt(web, r_b, geom):
    return burning_area(web,geom) * r_b # inner area times rate of regression (burn rate)

def throat_area(nozzle):
    return np.pi * nozzle.throat_radius**2 