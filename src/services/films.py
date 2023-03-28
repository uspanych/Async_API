from functools import lru_cache
from typing import List, Optional

from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.films import FilmDetailResponseModel, FilmResponseModel, FilmSort
from services.utils.body_elastic import get_body_search

from .base import BaseService


class FilmService(BaseService):
    async def get_by_id(
            self,
            film_id,
    ) -> Optional[FilmDetailResponseModel]:
        """Метод возвращает фильм по id."""

        return await self.get_data_by_id(
            film_id,
            'movies',
            self.FILM_CACHE_EXPIRE_IN_SECONDS,
        )

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
        body = get_body_search(
            size=page_size,
            sort_by='imdb_rating',
            offset=(page_size * page_number) - page_size,
            sort_order=sort_order,
            genre=genre,
            actor=actor,
            director=director,
            writer=writer
        )

        data_list = await self.get_list(
            index='movies',
            sort_by='imdb_rating',
            body=body,
            ttl=self.FILM_CACHE_EXPIRE_IN_SECONDS,
            sort_order=sort_order,
            page_size=page_size,
            page_number=page_number,
        )

        return data_list


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
