from functools import lru_cache

from pydantic import BaseSettings, AnyUrl


class Settings(BaseSettings):
    app_name: str = "Corona Travel Microservices"
    places_url: str = "http://localhost:1234"
    facts_url: str = "http://localhost:1234"
    map_2d_url: str = "http://localhost:1234"
    map_3d_url: str = "http://localhost:1234"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
