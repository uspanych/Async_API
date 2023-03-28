from enum import Enum
from typing import List, Optional

from models.base import BaseOrjsonModel



class FilmResponseModel(BaseOrjsonModel):
    id: str
    title: str
    imdb_rating: Optional[float] = None


class FilmDetailResponseModel(FilmResponseModel):
    genres: Optional[List[dict]] = None
    description: Optional[str] = None
    directors: Optional[List[str]] = None
    actors_names: Optional[List[str]] = None
    writers_names: Optional[List[str]] = None
    actors: Optional[List[dict]] = None
    writers: Optional[List[dict]] = None


class FilmSort(str, Enum):
    up_imdb_rating = "imdb_rating"
    down_imdb_rating = '-imdb_rating'
