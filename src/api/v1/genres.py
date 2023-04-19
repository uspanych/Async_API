from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query

from models.genres import (GenreDetailResponseModel, GenreResponseModel,
                           GenreSort)
from services.genres import GenreService, get_genre_service
from services.utils.constants import FILM_NOT_FOUND

router = APIRouter()


@router.get(
    "/{genre_id}",
    response_model=GenreDetailResponseModel,
    description="Метод, возвращающий жанр по его id"
)
async def genre_details(genre_id: str, genre_service: GenreService = Depends(get_genre_service)
                        ) -> GenreDetailResponseModel:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=FILM_NOT_FOUND)
    return genre


@router.get(
    '/',
    response_model=list[GenreResponseModel],
    description="Метод, возвращающий список жанров"
)
async def films_list(
    page_size: int = Query(50, gt=0),
    page_number: int = Query(1, gt=0),
    sort_by: GenreSort = GenreSort.down_name,
    genre_service: GenreService = Depends(get_genre_service),
) -> list[GenreResponseModel]:

    films = await genre_service.get_genres_list(
        page_size=page_size,
        page_number=page_number,
        sort_by=sort_by,
    )

    return films
