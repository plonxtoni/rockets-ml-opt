from dataclasses import dataclass

@dataclass
class ChamberState:
    P_c: float        # pressure in the chamber
    web: float        # web burned

