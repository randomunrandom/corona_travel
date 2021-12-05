from typing import List
from pydantic import BaseModel


class Position(BaseModel):
    lat: float
    lng: float


class PlaceWithoutID(BaseModel):
    name: str
    pos: Position

    class Config:
        schema_extra = {
            'example': {
                "name": "London",
                "pos": {
                    "lat": 51.509865,
                    "lng": -0.118092
                }
            }
        }


class Place(PlaceWithoutID):
    place_id: str

    class Config:
        schema_extra = {
            'example': {
                "name": "London",
                "pos": {
                    "lat": 51.509865,
                    "lng": -0.118092
                },
                "place_id": "lond"
            }
        }


Places = List[Place]
