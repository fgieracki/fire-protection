from sector import Sector
from typing import TypeAlias
from simulation.utils import Location

ForestMapCornerLocations: TypeAlias = tuple[Location, Location, Location, Location]


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

