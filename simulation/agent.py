from abc import ABC, abstractmethod
from datetime import datetime
from threading import Lock
from typing import TypeAlias, Union

from simulation.sector import Sector, SectorType
from fire_brigades.fire_brigade_state import FireBrigadeState
from forester_patrols.forester_patrol import ForesterPatrolState

from forest_map import ForestMap
from simulation.utils import Location

MovingAgentState: TypeAlias = Union[FireBrigadeState, ForesterPatrolState]


class Agent(ABC):
    def __init__(self, forest_map: ForestMap, timestamp: datetime, initial_location: Location) -> None:
        self.lock = Lock()
        self._timestamp = timestamp
        self._location = initial_location
        self._forest_map = forest_map

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @property
    def location(self) -> Location:
        return self._location

    @property
    def forest_map(self):
        return self._forest_map

    def find_sector(self) -> Sector:
        pass

    @abstractmethod
    def next(self, adjacent_sectors: list[Sector]) -> None:
        pass


class MovingAgent(Agent, ABC):
    def __init__(
        self,
        forest_map: ForestMap,
        timestamp: datetime,
        base_location: Location,
        initial_location: Location
    ):
        self._base_location = base_location
        Agent.__init__(self, forest_map, timestamp, initial_location)
        
    @property
    def base_location(self):
        return self._base_location

    @abstractmethod
    def move(self) -> None:
        pass


class SteadyAgent(Agent, ABC):
    def __init__(
        self,
        forest_map: ForestMap,
        timestamp: datetime,
        initial_location: Location
    ):
        Agent.__init__(self, forest_map, timestamp, initial_location)


def agent_worker(
        agent: Agent,
        row: int,
        column: int,
        sectors: list[list[Sector]]
) -> None:
    while True:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if not (
                    sectors[row + dr][column + dc] is SectorType.UNTRACKED
                    or sectors[row + dr][column + dc] is SectorType.WATER
                ):
                    pass
