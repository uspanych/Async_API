from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.persons import Person, PersonSort
from services.utils.body_elastic import get_body_search

from .base import BaseService

class PersonService(BaseService):
    async def get_genres_list(
            self,
            sort_by: PersonSort = PersonSort.down_full_name,
            page_size: int = 50,
            page_number: int = 1
    ) -> list[Person] | None:
        sort_order = 'desc' if sort_by == 'full_name' else 'asc'
        body = get_body_search(
            size=page_size,
            sort_by='full_name',
            offset=(page_size * page_number) - page_size,
            sort_order=sort_order
        )

        data_list = await self.get_list(
            index='persons',
            sort_by='full_name',
            body=body,
            ttl=self.FILM_CACHE_EXPIRE_IN_SECONDS,
            sort_order=sort_order,
            page_size=page_size,
            page_number=page_number,
        )

        return data_list


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
