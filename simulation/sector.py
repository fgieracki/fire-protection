from dataclasses import dataclass
from enum import Enum


class SectorType(Enum):
    DECIDUOUS = 1
    MIXED = 2
    CONIFEROUS = 3
    FIELD = 4
    FALLOW = 5
    WATER = 6
    UNTRACKED = 7


class GeographicDirection(Enum):
    N = 1
    NE = 2
    E = 3
    SE = 4
    S = 5
    SW = 6
    W = 7
    NW = 8


@dataclass
class SectorState:
    temperature: float | None
    wind_speed: float | None
    wind_direction: GeographicDirection | None
    air_humidity: int | None  # in percents
    plant_litter_moisture: int | None  # in percents
    co2_concentration: float | None  # parts per million
    pm2_5_concentration: float | None  # micrograms per cubic meter


class Sector:
    def __init__(
        self,
        sector_id: int,
        row: int,
        column: int,
        sector_type: SectorType,
        initial_state: SectorState
    ):
        self._sector_id = sector_id
        self._row = row
        self._column = column
        self._sector_type = sector_type
        self._state = initial_state

    @property
    def sector_id(self) -> int:
        return self._sector_id

    @property
    def row(self) -> int:
        return self._row

    @property
    def column(self) -> int:
        return self._column
    
    @property
    def sector_type(self) -> SectorType:
        return self._sector_type

    @property
    def state(self) -> SectorState:
        return self._state
