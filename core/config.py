from dataclasses import dataclass, field

@dataclass(frozen=True)
class Propellant:
    rho: float
    a: float
    n: float
    T_c: float
    gamma: float
    R: float


@dataclass(frozen=True)
class GrainGeometry:
    grain_type: str


@dataclass(frozen=True)
class BatesGrainGeometry(GrainGeometry):
    L0: float    # initial grain length
    r_i0: float  # initial inner radius
    r_o: float   # outer radius


@dataclass(frozen=True)
class Nozzle:
    throat_radius: float

    
@dataclass(frozen=True)
class CombustionModel:
    eta_cstar: float = 1.0
    eta_cf: float = 1.0


@dataclass
class MotorConfig:
    propellant: Propellant
    nozzle: Nozzle
    geom: GrainGeometry
    combustion: CombustionModel = field(default_factory=CombustionModel)