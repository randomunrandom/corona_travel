from json import loads

from .settings import Settings, get_settings
from .__version__ import __version__

from fastapi import FastAPI, HTTPException, Depends
from fastapi.openapi.utils import get_openapi
import httpx
from reusable_mongodb_connection import get_db
from mergedeep import merge

app = FastAPI(version=__version__, openapi_tags=[{"name": "root"}])


async def check_service(url: str) -> bool:
    async with httpx.AsyncClient() as client:
        return (await client.get(url)).is_success


@app.get("/test", tags=["root"])
async def test(settings: Settings = Depends(get_settings)):
    return {
        "name": settings.app_name,
        "can connect to microservice `places`": await check_service(
            f"{settings.places_url}/openapi.json"
        ),
        "can connect to microservice `facts`": await check_service(
            f"{settings.facts_url}/openapi.json"
        ),
        "can connect to microservice `map_2D`": await check_service(
            f"{settings.map_2d_url}/openapi.json"
        ),
        "can connect to microservice `map_3D`": await check_service(
            f"{settings.map_3d_url}/openapi.json"
        ),
    }


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    root_openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        tags=app.openapi_tags,
    )

    settings = get_settings()

    service2url = {
        "places": settings.places_url,
        "facts":  settings.facts_url,
        "map_2d": settings.map_2d_url,
        "map_3d": settings.map_3d_url,
    }
    service2openapi_schema = {k: loads(httpx.get(f"{v}/openapi.json").text) for k, v in service2url.items()}

    for dict_key in {"paths", "components"}:
        new_value = root_openapi_schema.get(dict_key, {})
        for v in service2openapi_schema.values():
            if dict_key in v:
                # maybe replace with iterative merge
                merge(new_value, v[dict_key])
        root_openapi_schema[dict_key] = new_value

    for list_key in {"tags"}:
        new_value = root_openapi_schema.get(list_key, [])
        for v in service2openapi_schema.values():
            if list_key in v:
                new_value += v[list_key]
        root_openapi_schema[list_key] = new_value


    # openapi_schema["info"]["x-logo"] = {
    #     "url": ""
    # }

    app.openapi_schema = root_openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
