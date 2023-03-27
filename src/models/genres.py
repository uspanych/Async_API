from src.models.base import BaseOrjsonModel


class GenreResponseModel(BaseOrjsonModel):
    id: str
    name: str


class GenreDetailResponseModel(GenreResponseModel):
    description: str
