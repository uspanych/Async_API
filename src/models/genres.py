from enum import Enum
from typing import Optional

from models.base import BaseOrjsonModel


class GenreResponseModel(BaseOrjsonModel):
    id: str
    name: str


class GenreDetailResponseModel(GenreResponseModel):
    description: Optional[str]


class GenreSort(str, Enum):
    up_name = "name"
    down_name = '-name'