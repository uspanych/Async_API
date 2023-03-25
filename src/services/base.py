from typing import Optional, Union, List
from elasticsearch import AsyncElasticsearch, NotFoundError
from redis.asyncio import Redis
import json
from services.utils.body_elastic import get_body_search


class BaseService:
    """Класс реализует базовые функции для возможных сервисов."""

    def __init__(
            self,
            redis: Redis,
            elastic: AsyncElasticsearch,
    ):
        self.redis = redis
        self.elastic = elastic

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
            sort_by: str,
            ttl: int = 300,
            sort_order: str = 'desc',
            page_size: int = 50,
            page_number: int = 1,
            genre: str = None,
            actor: str = None,
            director: str = None,
            writer: str = None,
    ):
        """Метод возвращает список записей."""

        cache_key = f'{index}-{sort_by}-{sort_order}-{page_size}-{page_number}'
        offset = (page_size * page_number) - page_size

        data = await self._data_from_cache(
            cache_key,
        )
        if not data:
            body = get_body_search(
                page_size,
                sort_by,
                offset,
                sort_order,
                genre,
                actor,
                director,
                writer,
            )

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
    ) -> List[dict]:
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