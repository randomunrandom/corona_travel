from typing import List
from enum import Enum

from pydantic import BaseModel


class Position(BaseModel):
    lat: float
    lng: float


class Marker3DType(str, Enum):
    fact = "fact"


class Marker3D(BaseModel):
    name: str
    marker_id: str
    type: Marker3DType
    pos: Position


Markers3D = List[Marker3D]
