from fastapi import APIRouter, Depends

from models.persons import Person, PersonSort
from services.persons import PersonService, get_person_service

router = APIRouter()


@router.get('/', response_model=list[Person])
async def persons_list(
    page_size: int,
    page_number: int,
    sort_by: PersonSort = PersonSort.down_full_name,
    genre_service: PersonService = Depends(get_person_service),
) -> list[Person]:

    films = await genre_service.get_genres_list(
        page_size=page_size,
        page_number=page_number,
        sort_by=sort_by,
    )

    return films
