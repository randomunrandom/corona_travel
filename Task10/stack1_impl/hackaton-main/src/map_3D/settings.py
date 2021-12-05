from functools import lru_cache
from typing import Any

from pydantic import BaseSettings


class Settings(BaseSettings):
    facts_url: Any = "http://localhost:1234"
    quizes_url: Any = "http://localhost:1234"
    excursions_url: Any = "http://localhost:1234"
    media_url: Any = "http://localhost:1234"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
