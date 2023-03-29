from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from http import HTTPStatus

from services.films import FilmService, get_film_service
from models.film import FilmSort, FilmResponseModel, FilmModel

router = APIRouter()


@router.get('/{film_id}', response_model=FilmModel)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> FilmModel:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return film


@router.get('/', response_model=List[FilmResponseModel])
async def films_list(
        page_size: int,
        page_number: int,
        genre: Optional[str] = None,
        actor: Optional[str] = None,
        writer: Optional[str] = None,
        director: Optional[str] = None,
        sort_by: FilmSort = FilmSort.down_imdb_rating,
        film_service: FilmService = Depends(get_film_service),
) -> List[FilmResponseModel]:
    films = await film_service.get_film_list(
        page_size=page_size,
        page_number=page_number,
        sort_by=sort_by,
        genre=genre,
        actor=actor,
        writer=writer,
        director=director,
    )

    return films
