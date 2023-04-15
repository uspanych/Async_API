from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from functional.settings import test_settings
from typing import List
import pytest
import pytest_asyncio
import asyncio


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def es_client():
    es_client = AsyncElasticsearch(hosts=test_settings.es_host)
    yield es_client
    await es_client.close()


@pytest_asyncio.fixture
async def es_create_scheme(es_client):
    async def inner(
            scheme: str,
            index: str,
    ):
        await es_client.indices.create(
            index=index,
            body=scheme,
        )

    return inner


@pytest_asyncio.fixture
async def es_write_data(es_client):
    async def inner(
            index: str,
            data: List[dict]
    ):
        document = []
        for item in data:
            document.append(
                {
                    "_index": index,
                    "_id": item.get('id'),
                    "_source": item,
                }
            )

        await async_bulk(es_client, document)

    return inner


@pytest_asyncio.fixture
async def es_delete_scheme(es_client):
    async def inner(
            index: str,
    ):
        await es_client.indices.delete(
            index=index,
        )

    return inner
