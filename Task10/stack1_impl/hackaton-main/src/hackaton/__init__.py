from fastapi import FastAPI

app = FastAPI()


@app.get("/{path}/")
def stats(path: str):
    return {"hello": "world"}
