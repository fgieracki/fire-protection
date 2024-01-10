from enum import Enum
from simulation.agent import MovingAgent
from simulation.forest_map import ForestMap
from simulation.sector import Sector
from simulation.utils import Location
from datetime import datetime


class ForesterPatrolState(Enum):
    AVAILABLE = 1
    TRAVELLING = 2
    PATROLLING = 3


class ForesterPatrol(MovingAgent):
    def __init__(
        self,
        forest_map: ForestMap,
        forester_patrol_id: str,
        timestamp: datetime,
        initial_state: ForesterPatrolState,
        base_location: Location,
        initial_location: Location
    ):
        self._forester_patrol_id = forester_patrol_id
        self._state = initial_state
        MovingAgent.__init__(self, forest_map, timestamp, base_location, initial_location)

    @property
    def forester_patrol_id(self) -> str:
        return self._forester_patrol_id

    @property
    def state(self) -> ForesterPatrolState:
        return self._state

    def next(self, adjacent_sectors: list[Sector]):
        pass

    def move(self) -> None:
        pass
