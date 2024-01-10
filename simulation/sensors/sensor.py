from .sensor_type import SensorType
from simulation.utils import Location
from datetime import datetime
from simulation.agent import SteadyAgent
from ..forest_map import ForestMap
from ..sector import Sector


class Sensor(SteadyAgent):
    def __init__(
        self,
        forest_map: ForestMap,
        timestamp: datetime,
        location: Location,
        sensor_id: str,
        sensor_type: SensorType,
        initial_data: [str, float],
    ) -> None:
        self._sensor_id = sensor_id
        self._sensor_type = sensor_type
        self._data = dict(initial_data)
        SteadyAgent.__init__(self, forest_map, timestamp, location)

    @property
    def sensor_id(self) -> str:
        return self._sensor_id

    @property
    def sensor_type(self) -> SensorType:
        return self._sensor_type
    
    @property
    def data(self) -> dict[str, float]:
        return self._data
    
    def next(self, adjacent_sectors: list[Sector]) -> None:
        pass

