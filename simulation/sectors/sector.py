import random
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
        self._sensors = []

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

    @extinguish_level.setter
    def extinguish_level(self, extinguish):
        self._extinguish_level = extinguish

    @property
    def sensors(self):
        return self._sensors

    def add_sensor(self, sensor):
        self._sensors.append(sensor)

    def remove_sensor(self, sensor):
        self._sensors.remove(sensor)

    def update_sensors(self):
        for sensor in self._sensors:
            if sensor['sensorType'] == "PM2_5":
                sensor['data'] = {
                    "pm2_5Concentration": self._state.pm2_5_concentration + random.uniform(-0.1, 0.1)
                }
            elif sensor['sensorType'] == "TEMPERATURE_AND_AIR_HUMIDITY":
                sensor['data'] = {
                    "temperature": self._state.temperature + random.uniform(-5.0, 5.0),
                    "airHumidity": self._state.air_humidity + random.uniform(-5.0, 5.0)
                }
            elif sensor['sensorType'] == "LITTER_MOISTURE":
                sensor['data'] = {
                    "plantLitterMoisture": self._state.plant_litter_moisture + random.uniform(-5.0, 5.0)
                }

            # TODO: add more sensor types
            print(sensor)
