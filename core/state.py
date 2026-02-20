from dataclasses import dataclass


@dataclass
class ChamberState:
    P_c: float  # pressure in the chamber
    web: float  # cumulative web/depth burned; assumed uniform everywhere (0D)
