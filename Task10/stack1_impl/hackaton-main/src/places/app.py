from typing import Optional, Any

from fastapi import FastAPI, HTTPException, Depends
from reusable_mongodb_connection import get_db

from .types import Place, PlaceWithoutID, Places
from .settings import Settings, get_settings

app = FastAPI(
    openapi_tags=[
        {
            "name": "resource:places",
        }
    ]
)


def get_places_collection(mongo_url: Any):
    try:
        db = get_db(mongo_url)
    except Exception as e:
        print("Connection to DB was unsuccessful")
        print(f"Exception: {e}")
        raise HTTPException(status_code=500, detail="Connection to DB was unsuccessful")

    if "places" not in db.list_collection_names():
        print("Collection not found")
        raise HTTPException(
            status_code=500,
            detail="Collection not found",
        )
    return db.places


@app.get("/places", response_model=Places, tags=["resource:places"])
def get_places(settings: Settings = Depends(get_settings)):
    place_collection = get_places_collection(settings.mongo_url)

    markers = place_collection.find({})

    res = []
    for m in markers:
        try:
            res.append(Place(**m))
        except Exception as e:
            print(str(e))
    return res


@app.post("/places", tags=["resource:places"])
def post_place(place: Place, settings: Settings = Depends(get_settings)):
    place_collection = get_places_collection(settings.mongo_url)

    place_with_same_id = place_collection.find_one({"place_id": place.place_id})

    if place_with_same_id is not None:
        raise HTTPException(status_code=400, detail="place ID occupied")

    place_collection.insert_one(place.dict())


@app.get("/places/{place_id}", response_model=Place, tags=["resource:places"])
def get_places_by_id(place_id: str, settings: Settings = Depends(get_settings)):
    collection = get_places_collection(settings.mongo_url)

    place = collection.find_one({"place_id": place_id})

    if place is None:
        raise HTTPException(
            status_code=404, detail="Place with specified id was not found"
        )
    return Place(**place)


@app.patch("/places/{place_id}", response_model=Place, tags=["resource:places"])
def patch_place(
    place_id: str,
    name: Optional[str] = None,
    lat: Optional[float] = None,
    lng: Optional[float] = None,
    settings: Settings = Depends(get_settings),
):
    places_collection = get_places_collection(settings.mongo_url)

    new_place_dict = {}
    if name is not None:
        new_place_dict["name"] = name
    if lat is not None:
        if "pos" not in new_place_dict:
            new_place_dict["pos"] = {}
        new_place_dict["pos"]["lat"] = lat
    if lng is not None:
        if "pos" not in new_place_dict:
            new_place_dict["pos"] = {}
        new_place_dict["pos"]["lng"] = lng

    if not new_place_dict:
        raise HTTPException(status_code=409, detail="No new parameters were supplied")

    res = places_collection.update_one({"place_id": place_id}, {"$set": new_place_dict})

    if not res.modified_count:
        raise HTTPException(status_code=409, detail="No new parameters were supplied")
    if not res.matched_count:
        raise HTTPException(
            status_code=404, detail="Place with specified ID was not found"
        )
    new_place = places_collection.find_one({"place_id": place_id})
    return Place(**new_place)


@app.put("/places/{place_id}", response_model=Place, tags=["resource:places"])
def put_place(
    place_id: str, place: PlaceWithoutID, settings: Settings = Depends(get_settings)
):
    places_collection = get_places_collection(settings.mongo_url)

    res = places_collection.update_one({"place_id": place_id}, {"$set": place.dict()})

    if not res.matched_count:
        raise HTTPException(
            status_code=404, detail="Place with specified ID was not found"
        )
    new_place = places_collection.find_one({"place_id": place_id})
    return Place(**new_place)


@app.delete("/places/{place_id}", tags=["resource:places"])
def delete_place(place_id: str, settings: Settings = Depends(get_settings)):
    places_collection = get_places_collection(settings.mongo_url)

    res = places_collection.delete_one({"place_id": place_id})

    if not res.deleted_count:
        raise HTTPException(
            status_code=404, detail="Place with specified ID was not found"
        )
