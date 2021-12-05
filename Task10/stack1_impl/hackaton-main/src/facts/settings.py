from functools import lru_cache

from pydantic import BaseSettings, AnyUrl


class Settings(BaseSettings):
    mongo_url: AnyUrl = "mongodb://localhost:27017/"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
