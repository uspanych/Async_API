import time

import pytest
import aiohttp
from functional.settings import test_settings


@pytest.mark.asyncio
async def test_search(es_write_data):
    session = aiohttp.ClientSession()
    url = 'http://127.0.0.1:8000/api/v1/films/search'
    query_data = {
        'query': 'Star',
    }
    time.sleep(1)

    async with session.get(url, params=query_data) as response:
        body = await response.json()

    await session.close()

    assert body
