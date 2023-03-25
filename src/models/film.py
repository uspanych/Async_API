import orjson
from typing import Optional, List
from pydantic import BaseModel
from enum import Enum


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class FilmResponseModel(BaseModel):
    id: str
    title: str
    imdb_rating: Optional[float] = None


class FilmModel(FilmResponseModel):
    genres: Optional[List[dict]] = None
    description: Optional[str] = None
    director: Optional[List[str]] = None
    actors_names: Optional[List[str]] = None
    writers_names: Optional[List[str]] = None
    actors: Optional[List[dict]] = None
    writers: Optional[List[dict]] = None

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class FilmSort(str, Enum):
    up_imdb_rating = "imdb_rating"
    down_imdb_rating = '-imdb_rating'


