from typing import Optional
from elasticsearch import AsyncElasticsearch, NotFoundError
from redis.asyncio import Redis
import json


class BaseService:
    """Класс реализует базовые функции для возможных сервисов."""

    def __init__(
            self,
            redis: Redis,
            elastic: AsyncElasticsearch,
    ):
        self.redis = redis
        self.elastic = elastic
        self.FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5

    async def get_data_by_id(
            self,
            data_id: str,
            index: str,
            ttl: int = 300,
    ):
        """Метод возвращает запись по id."""

        cache_key = f'{data_id}-{index}'
        data = await self._data_from_cache(
            cache_key,
        )

        if not data:
            data = await self._get_from_elastic(
                data_id,
                index,
            )
            if not data:
                return None

            await self._put_data_to_cache(
                cache_key,
                json.dumps(data),
                ttl,
            )

        return data

    async def get_list(
            self,
            index: str,
            body: str,
            sort_by: str = None,
            ttl: int = 300,
            sort_order: str = 'desc',
            page_size: int = 50,
            page_number: int = 1,
            genre: str = None,
            actor: str = None,
            director: str = None,
            writer: str = None,
            unique_key: str = None
    ):
        """Метод возвращает список записей."""

        cache_key = f'{index}-{sort_by}-{sort_order}-{page_size}-{page_number}-{genre}-{actor}-{director}-{writer}' \
                    f'-{unique_key}'

        data = await self._data_from_cache(
            cache_key,
        )
        if not data:
            data = await self._search_in_elastic(
                index,
                body,
            )
            if not data:
                return []

            await self._put_data_to_cache(
                cache_key,
                json.dumps(data),
                ttl,
            )

        return data

    async def search_by_query(
            self,
            index: str,
            body: str,
            query: str,
            ttl: int = 300,
            page_size: int = 50,
            page_number: int = 1,
    ):
        """Метод осуществляет поиск записей по query."""

        cache_key = f'{index}-{query}-{ttl}-{page_size}-{page_number}'

        data = await self._data_from_cache(
            cache_key,
        )

        if not data:
            data = await self._search_in_elastic(
                index,
                body,
            )
            if not data:
                return []

            await self._put_data_to_cache(
                cache_key,
                json.dumps(data),
                ttl,
            )

        return data

    async def _search_in_elastic(
            self,
            index: str,
            body: str,
    ) -> list[dict]:
        """Метод осуществляет поиск в Elasticsearch."""

        data = await self.elastic.search(
            index=index,
            body=body
        )

        return [item['_source'] for item in data['hits']['hits']]

    async def _get_from_elastic(
            self,
            data_id: str,
            index: str,
    ) -> Optional[dict]:
        """Метод осуществляет поиск в Elasticsearch по id."""

        try:
            doc = await self.elastic.get(index, data_id)

        except NotFoundError:
            return None

        return doc['_source']

    async def _data_from_cache(
            self,
            key: str
    ) -> Optional[dict]:
        """Метод возвращает данные из кеша."""

        data = await self.redis.get(key)
        if not data:
            return None

        return json.loads(data)

    async def _put_data_to_cache(
            self,
            key: str,
            value,
            ttl: int,
    ) -> None:
        """Метод сохраняет данные в кеш."""

        await self.redis.set(
            key,
            value,
            ttl,
        )
