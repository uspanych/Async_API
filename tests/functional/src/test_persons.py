import pytest
import aiohttp
from functional.settings import test_settings


@pytest.mark.asyncio
async def test_get_all_persons(es_write_data):
    session = aiohttp.ClientSession()
    url = test_settings.service_url + '/api/v1/persons'

    async with session.get(url) as response:
        body = await response.json()

        assert response.status == 200
        assert len(body) == 6
        assert body[0]['full_name'] == "Biba"


@pytest.mark.asyncio
async def test_get_all_persons_first_page(es_write_data):
    session = aiohttp.ClientSession()
    url = test_settings.service_url + '/api/v1/persons'

    async with session.get(url, params=dict(page_number=1, page_size=1)) as response:
        body = await response.json()

        assert response.status == 200
        assert len(body) == 1
        assert body[0]['full_name'] == "Biba"


@pytest.mark.asyncio
async def test_get_all_persons_desc(es_write_data):
    session = aiohttp.ClientSession()
    url = test_settings.service_url + '/api/v1/persons'

    async with session.get(url, params=dict(sort_by="full_name")) as response:
        body = await response.json()

        assert response.status == 200
        assert len(body) == 6
        assert body[0]['full_name'] == "Stive Jobs"


@pytest.mark.parametrize(
    'id',
    [
        222,
        111,
        333,
        123,
        444,
        112,
    ]
)
@pytest.mark.asyncio
async def test_get_persons_by_id(es_write_data, id):
    session = aiohttp.ClientSession()
    url = test_settings.service_url + f'/api/v1/persons/{id}'

    async with session.get(url) as response:
        body = await response.json()

        assert response.status == 200
        assert str(body['id']) == str(id)


@pytest.mark.parametrize(
    'id',
    [
        222,
        111,
        333,
        123,
        444,
        112,
    ]
)
@pytest.mark.asyncio
async def test_get_films_of_person_by_id(es_write_data, id):
    session = aiohttp.ClientSession()
    url = test_settings.service_url + f'/api/v1/persons/{id}/film'

    async with session.get(url) as response:
        body = await response.json()

        assert response.status == 200
        assert len(body) == 10


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'query': 'Kelvin Clein'},
                {'status': 200, 'length': 1}
        ),
        (
                {'query': 'Mashed potato'},
                {'status': 200, 'length': 0}
        ),
    ]
)
@pytest.mark.asyncio
async def test_person_search(es_write_data, query_data, expected_answer):
    session = aiohttp.ClientSession()
    url = test_settings.service_url + '/api/v1/persons/persons/search'

    async with session.get(url, params=query_data) as response:
        body = await response.json()

        assert len(body) == expected_answer['length']
        assert response.status == expected_answer['status']


    await session.close()
