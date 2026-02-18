from dataclasses import dataclass

@dataclass
class ChamberState:
    P: float        # pressure in the chamber
    web: float      # web thickness
