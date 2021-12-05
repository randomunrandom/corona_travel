from typing import List
from pydantic import BaseModel


class Position(BaseModel):
    lat: float
    lng: float


class Marker2D(BaseModel):
    name: str
    place_id: str
    pos: Position


Markers2D = List[Marker2D]
