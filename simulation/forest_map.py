import json

from simulation.sectors.sector import Sector
from typing import TypeAlias
from simulation.location import Location
from simulation.sectors.sector_state import SectorState
from simulation.sectors.sector_type import SectorType

ForestMapCornerLocations: TypeAlias = tuple[Location, Location, Location, Location]  # cw start upper left


class ForestMap:
    def __init__(
        self,
        forest_id: str,
        forest_name: str,
        height: int,
        width: int,
        location: ForestMapCornerLocations,
        sectors: list[list[Sector]]
    ):
        self._forest_id = forest_id
        self._forest_name = forest_name
        self._height = height
        self._width = width
        self._location = location
        self._sectors = sectors



    @classmethod
    def from_conf(cls, conf_file: str):
        with open(conf_file, 'r') as fp:
            conf = json.load(fp)

        locations = conf["location"]
        sectors_:list[list[Sector | None]] = [[None for _ in range(conf["width"] // conf["sectorSize"] + 1)] for _ in range(conf["height"] // conf["sectorSize"] + 1)]
        for val in conf["sectors"]:
            print(val)
            initial_state = SectorState(
                temperature=val["initialState"]["temperature"],
                wind_speed=val["initialState"]["windSpeed"],
                wind_direction=val["initialState"]["windDirection"],
                air_humidity=val["initialState"]["airHumidity"],
                plant_litter_moisture=val["initialState"]["plantLitterMoisture"],
                co2_concentration=val["initialState"]["co2Concentration"],
                pm2_5_concentration=val["initialState"]["pm2_5Concentration"],
            )

            if SectorType[val["sectorType"]] is None:
                print(val["sectorType"])

            sectors_[val["row"]-1][val["column"]-1] = Sector(
                sector_id=val["sectorId"],
                row=val["row"]-1,
                column=val["column"]-1,
                sector_type= SectorType[val["sectorType"]],
                initial_state=initial_state,
            )



        values = {
            "forest_id": conf["forestId"],
            "forest_name": conf["forestName"],
            "height": conf["height"],
            "width": conf["width"],
            "location": (
                tuple(Location(**location) for location in locations)
            ),
            "sectors": sectors_
        }

        # parse this json to object:
        # "sensors": [
        #     {
        #         "sensorId": 0,
        #         "sensorType": 1,
        #         "location": {
        #             "longitude": 50.5,
        #             "latitude": 50.5
        #         },
        #         "timestamp": "<built-in method now of type object at 0x1025c8980>"
        #     },
        #     {
        #         "sensorId": 3,
        #         "sensorType": 1,
        #         "location": {
        #             "longitude": 50.5,
        #             "latitude": 51.5
        #         },
        #         "timestamp": "<built-in method now of type object at 0x1025c8980>"
        #     },





        return ForestMap(**values)

    @property
    def forest_id(self) -> str:
        return self._forest_id

    @property
    def forest_name(self) -> str:
        return self._forest_name

    @property
    def height(self) -> int:
        return self._height

    @property
    def width(self) -> int:
        return self._width

    @property
    def location(self) -> ForestMapCornerLocations:
        return self._location

    @property
    def sectors(self) -> list[list[Sector]]:
        return self._sectors
    
    def get_sector_with_max_burn_level(self) -> Sector:
        max_burn_level = 0
        max_burn_sector = None
        for row in self._sectors:
            for sector in row:
                if sector.burn_level > max_burn_level:
                    max_burn_level = sector.burn_level
                    max_burn_sector = sector
        return max_burn_sector
    
    def get_sector_location(self, sector: Sector) -> Location:

        return Location(
            longitude=self._location[0].longitude + sector.column * (self._location[1].longitude - self._location[0].longitude) / self._width,
            latitude=self._location[0].latitude + sector.row * (self._location[2].latitude - self._location[1].latitude) / self._height
        )
    
    def get_sector(self, sector_id: int) -> Sector:
        for row in self._sectors:
            for sector in row:
                if sector.sector_id == sector_id:
                    return sector
        return None

    def find_sector(self, location: Location):
        lat_interpolation = (
                (location.latitude - self._location[1].latitude)
                / (self._location[2].latitude - self._location[1].latitude)
        )
        lon_interpolation = (
                (location.longitude - self._location[0].longitude)
                / (self._location[1].longitude - self._location[0].longitude)
        )

        height_index = int(self._height * lat_interpolation)
        width_index = int(self._width * lon_interpolation)

        return self._sectors[height_index][width_index]

    def get_adjacent_sectors(self, sector: Sector, old_sectors: list[list[Sector]]) -> list[Sector]:
        row = sector.row
        column = sector.column
        adjacent_sectors = []

        if row > 0:
            adjacent_sectors.append(old_sectors[row - 1][column])
        if row < len(old_sectors) - 1:
            adjacent_sectors.append(old_sectors[row + 1][column])
        if column > 0:
            adjacent_sectors.append(old_sectors[row][column - 1])
        if column < len(old_sectors[1]) - 1:
            adjacent_sectors.append(old_sectors[row][column + 1])

        # for row_index in range(max(row - 1, 0), min(row + 1, self.height - 1)):
        #     for column_index in range(max(column - 1, 0), min(column + 1, self.width - 1)):
        #         adjacent_sectors.append(self._sectors[row_index][column_index])

        return adjacent_sectors
