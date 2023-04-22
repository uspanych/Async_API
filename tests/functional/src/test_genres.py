import pytest
import aiohttp
from functional.settings import test_settings


@pytest.mark.asyncio
async def test_get_all_genres(es_write_data):
    session = aiohttp.ClientSession()
    url = test_settings.service_url + '/api/v1/genres'

    async with session.get(url) as response:
        body = await response.json()

        assert response.status == 200
        assert len(body) == 2
        assert body[0]['name'] == "Action"


@pytest.mark.asyncio
async def test_get_all_genres_first_page(es_write_data):
    session = aiohttp.ClientSession()
    url = test_settings.service_url + '/api/v1/genres'

    async with session.get(url, params=dict(page_number=1, page_size=1)) as response:
        body = await response.json()

        assert response.status == 200
        assert len(body) == 1
        assert body[0]['name'] == "Action"


@pytest.mark.asyncio
async def test_get_all_genres_desc(es_write_data):
    session = aiohttp.ClientSession()
    url = test_settings.service_url + '/api/v1/genres'

    async with session.get(url, params=dict(sort_by="name")) as response:
        body = await response.json()

        assert response.status == 200
        assert len(body) == 2
        assert body[0]['name'] == "Sci-Fi"


@pytest.mark.parametrize(
    'id',
    [
        566,
        679,
    ]
)
@pytest.mark.asyncio
async def test_get_genre_by_id(es_write_data, id):
    session = aiohttp.ClientSession()
    url = test_settings.service_url + f'/api/v1/genres/{id}'

    async with session.get(url) as response:
        body = await response.json()

        assert response.status == 200
        assert str(body['id']) == str(id)
