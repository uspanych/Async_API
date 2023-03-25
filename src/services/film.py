from functools import lru_cache
from typing import Optional, List
from .base import BaseService
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from redis.asyncio import Redis
from models.film import FilmModel, FilmSort, FilmResponseModel
from db.elastic import get_elastic
from db.redis import get_redis

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class FilmService(BaseService):
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        super().__init__(
            redis,
            elastic,
        )

    async def get_by_id(
            self,
            film_id,
    ) -> Optional[FilmModel]:
        """Метод возвращает фильм по id."""

        data = await self.get_data_by_id(
            film_id,
            'movies',
            FILM_CACHE_EXPIRE_IN_SECONDS,
        )

        return FilmModel(**data)

    async def get_film_list(
            self,
            sort_by: FilmSort = FilmSort.down_imdb_rating,
            page_size: int = 50,
            page_number: int = 1,
            genre: str = None,
            actor: str = None,
            director: str = None,
            writer: str = None,
    ) -> List[Optional[FilmResponseModel]]:
        """Метод возвращает список фильмов."""

        sort_order = 'desc' if sort_by == 'imdb_rating' else 'asc'

        data_list = await self.get_list(
            index='movies',
            sort_by='imdb_rating',
            sort_order=sort_order,
            ttl=FILM_CACHE_EXPIRE_IN_SECONDS,
            page_size=page_size,
            page_number=page_number,
            genre=genre,
            actor=actor,
            director=director,
            writer=writer,
        )

        return [FilmResponseModel(**item) for item in data_list]


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
