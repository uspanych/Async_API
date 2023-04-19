import pytest
import aiohttp
from functional.settings import test_settings


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'search': 'The Star'},
                {'status': 200, 'length': 50}
        ),
        (
                {'search': 'Mashed potato'},
                {'status': 200, 'length': 0}
        ),
    ]
)
@pytest.mark.asyncio
async def test_search(es_write_data, query_data, expected_answer):
    session = aiohttp.ClientSession()
    url = test_settings.service_url + '/api/v1/films/search'
    query_data = {
        'query': 'Star',
    }

    async with session.get(url, params=query_data) as response:
        body = await response.json()

    await session.close()
