from dataclasses import dataclass

@dataclass(frozen=True)
class Propellant:
    rho: float
    a: float
    n: float
    Tc: float
    gamma: float
    R: float

@dataclass(frozen=True)
class BatesGrainGeometry(GrainGeometry):
    L: float
    r_i0: float
    r_o: float

@dataclass(frozen=True)
class GrainGeometry:
    grain_type: str

@dataclass(frozen=True)
class Nozzle:
    throat_radius: float


@dataclass
class MotorConfig:
    propellant: Propellant
    nozzle: Nozzle
    grgeom: GrainGeometry