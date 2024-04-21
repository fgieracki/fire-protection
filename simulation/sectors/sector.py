from threading import Lock

from simulation.sectors.sector_state import SectorState
from simulation.sectors.sector_type import SectorType


class Sector:
    def __init__(
        self,
        sector_id: int,
        row: int,
        column: int,
        sector_type: SectorType,
        initial_state: SectorState
    ):
        self.lock = Lock()
        self._sector_id = sector_id
        self._row = row
        self._column = column
        self._sector_type = sector_type
        self._state = initial_state
        self._extinguish_level = 0 #scale 0-100
        self._burn_level = 0 #scale 0-100

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

    @property
    def extinguish_level(self) -> int:
        return self._extinguish_level

    @property
    def burn_level(self) -> int:
        return self._burn_level

    @burn_level.setter
    def burn_level(self, burn):
        self._burn_level = burn