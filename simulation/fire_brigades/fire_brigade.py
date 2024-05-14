import logging
from datetime import datetime
import json

from simulation.agent import MovingAgent
from simulation.forest_map import ForestMap
from simulation.location import Location
from simulation.fire_brigades.fire_brigade_state import FireBrigadeState


class FireBrigade(MovingAgent):
    def __init__(
        self,
        # forest_map: ForestMap, #think how to get it easily
        fire_brigade_id: str,
        timestamp: datetime,
        initial_state: FireBrigadeState,
        base_location: Location,
        initial_location: Location,
        destination: Location
    ):
        # MovingAgent.__init__(self, forest_map, timestamp, base_location, initial_location, destination)
        self._fire_brigade_id = fire_brigade_id
        self._state = initial_state
        self._destination = destination

    @property
    def fire_brigade_id(self) -> str:
        return self._fire_brigade_id

    @property
    def state(self) -> FireBrigadeState:
        return self._state
    
    @property
    def destination(self) -> Location:
        return self._destination
    
    @classmethod
    def from_conf(cls, conf_file: str):
        with open(conf_file, 'r') as fp:
            conf = json.load(fp)

        fire_brigades = []
        for val in conf["fireBrigades"]:
            fire_brigade_id=val["fireBrigadeId"],
            timestamp=val["timestamp"],
            initial_state=val["initialState"],
            base_location=Location(**val["baseLocation"]),
            initial_location=Location(**val["initialLocation"]),
            destination=Location(**val["destination"])
            print(fire_brigade_id[0], timestamp, FireBrigadeState(initial_state[0]), base_location, initial_location, destination)
            fire_brigades.append(cls(fire_brigade_id[0], timestamp, FireBrigadeState(initial_state[0]), base_location, initial_location, destination))

        return fire_brigades

    def next(self):
        pass

    def move(self, next_destination=None) -> None:
        # if next_destination is None:
        #     next_destination = self._destination
            
        if self._state == FireBrigadeState.AVAILABLE and next_destination != None:
            self._state = FireBrigadeState.TRAVELLING
            self._destination = next_destination
            print('Fire brigade is travelling to the fire.')

        elif self._state == FireBrigadeState.TRAVELLING:
            if self._destination == self._base_location:
                self._state = FireBrigadeState.AVAILABLE
                print('Fire brigade has returned to the base.')
            elif self._destination == self._initial_location:
                self._state = FireBrigadeState.EXTINGUISHING

            if next_destination != None:
                self._destination = next_destination

        elif self._state == FireBrigadeState.EXTINGUISHING:
            self._state = FireBrigadeState.AVAILABLE
            self._destination = self._base_location

        self.log()

    def log(self) -> None:
        print(f'Fire brigade {self._fire_brigade_id} is in state: {self._state}.')
        logging.debug(f'Fire brigade {self._fire_brigade_id} is in state: {self._state}.')
