from src.models.base import BaseOrjsonModel


class Person(BaseOrjsonModel):
    id: str
    full_name: str
