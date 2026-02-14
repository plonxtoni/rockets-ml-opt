@dataclass(frozen=True)
class Propellant:
    rho: float
    a: float
    n: float
    Tc: float
    gamma: float
    R: float


@dataclass(frozen=True)
class GrainGeometry:
    L0: float
    ri0: float
    ro: float


@dataclass(frozen=True)
class Nozzle:
    throat_radius: float
