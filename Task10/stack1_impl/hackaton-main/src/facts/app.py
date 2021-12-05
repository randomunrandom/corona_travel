from typing import Optional, Any

from fastapi import FastAPI, HTTPException, Depends
from reusable_mongodb_connection import get_db

from .types import Fact, FactWithoutId, Facts
from .settings import Settings, get_settings

app = FastAPI(openapi_tags=[{"name": "resource:facts"}])


def get_facts_collection(mongo_url: Any):
    try:
        db = get_db(mongo_url)
    except Exception as e:
        print("Connection to DB was unsuccesfull")
        print(f"Exception: {e}")
        raise HTTPException(status_code=500, detail="Connection to DB was unsuccesfull")

    if "facts" not in db.list_collection_names():
        print("Collection not found")
        raise HTTPException(
            status_code=500,
            detail="Collection not found",
        )

    return db.facts


@app.get("/facts", response_model=Facts, tags=["resource:facts"])
def get_facts(settings: Settings = Depends(get_settings)):
    facts_collection = get_facts_collection(settings.mongo_url)
    facts = facts_collection.find({})

    res = []
    for f in facts:
        try:
            res.append(Fact(**f))
        except Exception as e:
            print(str(e))
    return res


@app.post("/facts", tags=["resource:facts"])
def post_fact(fact: Fact, settings: Settings = Depends(get_settings)):
    facts_collection = get_facts_collection(settings.mongo_url)

    fact_with_same_id = facts_collection.find_one({"fact_id": fact.fact_id})

    if fact_with_same_id is not None:
        raise HTTPException(status_code=400, detail="fact ID occupied")

    facts_collection.insert_one(fact.dict())


@app.get("/facts/{fact_id}", response_model=Fact, tags=["resource:facts"])
def get_fact_by_id(fact_id: str, settings: Settings = Depends(get_settings)):
    facts_collection = get_facts_collection(settings.mongo_url)

    fact = facts_collection.find_one({"fact_id": fact_id})

    if fact is None:
        raise HTTPException(
            status_code=404, detail="Fact with specified id was not found"
        )
    return Fact(**fact)


@app.patch("/facts/{fact_id}", response_model=Fact, tags=["resource:facts"])
def patch_fact(
    fact_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    lat: Optional[float] = None,
    lng: Optional[float] = None,
    settings: Settings = Depends(get_settings),
):
    new_fact_dict = {}
    if name is not None:
        new_fact_dict["name"] = name
    if description is not None:
        new_fact_dict["description"] = description
    if lat is not None:
        if "pos" not in new_fact_dict:
            new_fact_dict["pos"] = {}
        new_fact_dict["pos"]["lat"] = lat
    if lng is not None:
        if "pos" not in new_fact_dict:
            new_fact_dict["pos"] = {}
        new_fact_dict["pos"]["lng"] = lng

    if not new_fact_dict:
        raise HTTPException(status_code=409, detail="No new parameters were supplied")

    facts_collection = get_facts_collection(settings.mongo_url)

    result = facts_collection.update_one({"fact_id": fact_id}, {"$set": new_fact_dict})

    if result.matched_count != 1:
        raise HTTPException(
            status_code=404, detail="Fact with specified id was not found"
        )
    if result.modified_count != 1:
        raise HTTPException(status_code=409, detail="No new parameters were supplied")
    new_fact = facts_collection.find_one({"fact_id": fact_id})
    return Fact(**new_fact)


@app.put("/facts/{fact_id}", response_model=Fact, tags=["resource:facts"])
def put_fact(
    fact_id: str, fact: FactWithoutId, settings: Settings = Depends(get_settings)
):
    facts_collection = get_facts_collection(settings.mongo_url)

    result = facts_collection.replace_one(
        {"fact_id": fact_id},
        {"fact_id": fact_id, "name": fact.name, "description": fact.description, "pos": fact.pos.dict()},
    )

    if result.matched_count != 1:
        raise HTTPException(
            status_code=404, detail="Fact with specified ID was not found"
        )
    return {"fact_id": fact_id, "name": fact.name, "description": fact.description, "pos": fact.pos.dict()}


@app.delete("/fact/{fact_id}", tags=["resource:facts"])
def delete_fact(fact_id: str, settings: Settings = Depends(get_settings)):
    facts_collection = get_facts_collection(settings.mongo_url)

    res = facts_collection.delete_one({"fact_id": fact_id})

    if res.deleted_count != 1:
        raise HTTPException(
            status_code=404, detail="Fact with specified id was not found"
        )
