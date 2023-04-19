from functools import lru_cache
from pprint import pprint

from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.films import FilmDetailResponseModel, FilmResponseModel, FilmSort
from services.utils.body_elastic import get_body_search, get_body_query
from .base import BaseService


class FilmService(BaseService):
    """Сервис реализует возможности получения фильмов."""

    async def get_by_id(
            self,
            film_id,
    ) -> FilmDetailResponseModel | None:
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
    ) -> list[FilmResponseModel | None]:
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

        pprint(body)

        data_list = await self.get_list(
            index='movies',
            sort_by='imdb_rating',
            sort_order=sort_order,
            ttl=self.FILM_CACHE_EXPIRE_IN_SECONDS,
            body=body,
            page_size=page_size,
            page_number=page_number,
            genre=genre,
            actor=actor,
            director=director,
            writer=writer
        )

        return data_list

    async def search_film_by_query(
            self,
            query,
            page_size: int = 50,
            page_number: int = 1,

    ) -> list[FilmResponseModel | None]:
        """Метод вовзращает список найденных фильмов."""

        body = get_body_query(
            field='title',
            value=query,
            size=page_size,
            offset=(page_size * page_number) - page_size,
        )

        data_list = await self.search_by_query(
            index='movies',
            body=body,
            query=query,
            ttl=self.FILM_CACHE_EXPIRE_IN_SECONDS,
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
