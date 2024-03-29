from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class UUIDMixin(BaseModel):
    id: str


class ModifiedMixin(UUIDMixin):
    modified: datetime


class IndexMixin(BaseModel):
    index: str


class PostgresModel(ModifiedMixin, UUIDMixin):
    pass


class PersonModel(UUIDMixin, IndexMixin):
    full_name: str


class GenreModel(UUIDMixin, IndexMixin):
    name: str
    description: Optional[str] = None


class ToElasticModel(UUIDMixin, IndexMixin):
    imdb_rating: Optional[float] = None
    genres: Optional[List[dict]] = None
    title: str
    description: Optional[str] = None
    directors: Optional[List[dict]] = None
    actors_names: Optional[List[str]] = None
    writers_names: Optional[List[str]] = None
    actors: Optional[List[dict]] = None
    writers: Optional[List[dict]] = None
