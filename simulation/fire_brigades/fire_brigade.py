import logging
from datetime import datetime

from simulation.agent import MovingAgent
from simulation.forest_map import ForestMap
from simulation.location import Location
from simulation.fire_brigades.fire_brigade_state import FireBrigadeState


class FireBrigade(MovingAgent):
    def __init__(
        self,
        forest_map: ForestMap,
        fire_brigade_id: str,
        timestamp: datetime,
        initial_state: FireBrigadeState,
        base_location: Location,
        initial_location: Location
    ):
        MovingAgent.__init__(self, forest_map, timestamp, base_location, initial_location)
        self._fire_brigade_id = fire_brigade_id
        self._state = initial_state

    @property
    def fire_brigade_id(self) -> str:
        return self._fire_brigade_id

    @property
    def state(self) -> FireBrigadeState:
        return self._state

    def next(self):
        pass

    def move(self) -> None:
        pass

    def log(self) -> None:
        logging.debug(f'Fire brigade {self._fire_brigade_id} is in state: {self._state}.')
