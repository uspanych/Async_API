from fastapi import APIRouter, Depends, Query, HTTPException
from http import HTTPStatus
from models.films import FilmResponseModel
from models.persons import Person, PersonSort, PersonPage
from services.persons import PersonService, get_person_service
from services.utils.constants import FILM_NOT_FOUND

router = APIRouter()


@router.get(
    '/persons/search',
    response_model=list[PersonPage],
    description='Метод, выполняет поиск по запросу'
)
async def search_person(
        query: str,
        page_size: int = Query(..., gt=0),
        page_number: int = Query(..., gt=0),
        person_service: PersonService = Depends(get_person_service)
) -> list[PersonPage]:

    persons = await person_service.search_person_with_films(
        query=query,
        page_size=page_size,
        page_number=page_number,
    )

    return persons


@router.get(
    '/{person_id}/film',
    response_model=list[FilmResponseModel],
    description="Метод, возвращает список фильмов по персоне"
)
async def films_persons(
        person_id: str, person_service: PersonService = Depends(get_person_service)
) -> FilmResponseModel:
    films = await person_service.get_films_with_person(
        person_id=person_id,
    )
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=FILM_NOT_FOUND)
    return films


@router.get(
    '/',
    response_model=list[Person],
    description="Метод, возвращающий список персон"
)
async def persons_list(
        page_size: int = Query(..., gt=0),
        page_number: int = Query(..., gt=0),
        sort_by: PersonSort = PersonSort.down_full_name,
        person_service: PersonService = Depends(get_person_service),
) -> list[Person]:
    persons = await person_service.get_persons_list(
        page_size=page_size,
        page_number=page_number,
        sort_by=sort_by,
    )

    return persons


@router.get(
    "/{person_id}",
    response_model=PersonPage,
    description="Метод, возвращающий персону по его id"
)
async def person_details(person_id: str, person_service: PersonService = Depends(get_person_service)
                         ) -> Person:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=FILM_NOT_FOUND)
    return person
