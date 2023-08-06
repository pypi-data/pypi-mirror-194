from dataclasses import dataclass
from typing import List
from enum import Enum


class Region(Enum):
    Europe = 1
    America = 2
    Switzerland = 3
    Singapore = 4
    Custom = 5


@dataclass(init=True)
class RegionUri:
    region: Region
    ha_uri: str
    urls: List[str]


def region_resolve(region: Region, uris: List[RegionUri]) -> RegionUri:
    for x in uris:
        if x.region == region:
            return x
    return None
