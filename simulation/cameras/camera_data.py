from dataclasses import dataclass
from simulation.utils import Location


@dataclass
class CameraData:
    smoke_detected: bool
    smoke_level: int
    smoke_location: Location
