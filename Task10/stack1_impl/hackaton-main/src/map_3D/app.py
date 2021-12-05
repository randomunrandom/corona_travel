from json import loads
import asyncio
from typing import Any, Awaitable, Callable
import math
from logging import getLogger

from fastapi import FastAPI, Depends, HTTPException, status
import httpx

from .types import Marker3D, Markers3D, Position
from .settings import Settings, get_settings

app = FastAPI(openapi_tags=[{"name": "service:map3D"}])

logger = getLogger("service:map3D")


def deg2rad(deg: float) -> float:
    return deg * (math.pi / 180)


def check_pos(obj_pos: Position, cur_pos: Position, distance: float) -> bool:
    R: int = 6371  # Radius of the earth in km
    dLat: float = deg2rad(obj_pos.lat - cur_pos.lat)
    dLon: float = deg2rad(obj_pos.lng - cur_pos.lng)

    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(
        deg2rad(cur_pos.lat)
    ) * math.cos(deg2rad(obj_pos.lat)) * math.sin(dLon / 2) * math.sin(dLon / 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c  # Distance in km
    logger.debug("distance is %s", d)
    if d * 1000 <= distance:
        return True
    return False


def type_obj2id(obj_type: str, obj: Any) -> str:
    if obj_type == "fact":
        return obj["fact_id"]


def get_url_factory(
    position: Position, distance: float
) -> Callable[[tuple[str, str]], Awaitable[Markers3D]]:
    async def get_url(url_type_and_string: tuple[str, str]) -> Markers3D:
        url_type, url = url_type_and_string

        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        # if response.status_code != 200:
        #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        objs = loads(response.text)

        correct_objects = [
            o for o in objs if check_pos(Position(**o["pos"]), position, distance)
        ]

        res = [
            Marker3D(
                type=url_type,
                name=o["name"],
                marker_id=type_obj2id(url_type, o),
                pos=o["pos"],
            )
            for o in correct_objects
        ]
        return res

    return get_url


@app.get("/map/3D/{lat}/{lng}", response_model=Markers3D, tags=["service:map3D"])
async def map3D(
    lat: float,
    lng: float,
    distance: float = 20,
    settings: Settings = Depends(get_settings),
):
    """get markers for 3D map

    Parameters
    ----------
    lat: float
        current latitude
    lng: float
        current longitude
    distance: float, optional
        distance in meters, default is 20

    Returns
    -------
    Markers
        list of markers for 3D map
    """
    type2url: dict[str, str] = {
        "fact": f"{settings.facts_url}/facts",
    }
    cur_position = Position(lat=lat, lng=lng)

    markers: Markers3D = [
        marker
        for markers in await asyncio.gather(
            *map(get_url_factory(cur_position, distance), type2url.items())
        )
        for marker in markers
    ]
    return markers
