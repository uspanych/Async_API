import pytest
import aiohttp
from functional.settings import test_settings


@pytest.mark.asyncio
async def test_get_all_persons(es_write_data):
    session = aiohttp.ClientSession()
    url = test_settings.service_url + '/api/v1/films'

    async with session.get(url) as response:
        body = await response.json()

        assert response.status == 200
        assert len(body) == 50
        assert body[0]['title'] == "The Star"


@pytest.mark.asyncio
async def test_get_all_persons_first_page(es_write_data):
    session = aiohttp.ClientSession()
    url = test_settings.service_url + '/api/v1/films'

    async with session.get(url, params=dict(page_number=1, page_size=1)) as response:
        body = await response.json()

        assert response.status == 200
        assert len(body) == 1
        assert body[0]['title'] == "The Star"


@pytest.mark.parametrize(
    'id',
    [
        "1f90980e-e7c9-4fac-a1e4-f34409daeff2",
    ]
)
@pytest.mark.asyncio
async def test_get_film_by_id(es_write_data, id):
    session = aiohttp.ClientSession()
    url = test_settings.service_url + f'/api/v1/films/{id}'

    async with session.get(url) as response:
        body = await response.json()

        assert response.status == 200
        assert body["id"] == id
