from datetime import date
from fastapi import APIRouter, Body, Query, HTTPException
from fastapi_cache.decorator import cache

from src.exceptions import WrongDatesException, ObjectNotFoundException
from src.schemas.hotels import HotelPatch, HotelAdd
from src.api.dependencies import PaginationDep, DBDep
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    "",
    summary="Получить свободные отели по дате",
    description="Получить свободные отели на указанный промежуток дат. Фильтрация по названию и местоположению",
)
@cache(expire=60)
async def hotels_get_by_date(
    db: DBDep,
    pagination: PaginationDep,
    date_from: date = Query(default="2024-12-20"),
    date_to: date = Query(default="2024-12-30"),
    title: str | None = None,
    location: str | None = None,
):
    try:
        free_hotels = await HotelService(db).get_free_hotels_by_date_service(
            pagination, date_from, date_to, title, location
        )
    except WrongDatesException as exc:
        raise HTTPException(422, exc.detail)
    return {"free_hotels_for_these_dates": free_hotels}


@router.get("/{hotel_id}", summary="Получить отель по ID")
async def hotel_get_by_id(db: DBDep, hotel_id: int):
    hotel = await HotelService(db).hotel_get_by_id_service(hotel_id)
    if not hotel:
        raise HTTPException(404, "Нет отеля с таким ID")
    return hotel


@router.post("", summary="Добавить отель")
async def hotel_add(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Rome",
                "value": {
                    "title": "Coliseum Five Stars",
                    "location": "Rome, Italy",
                },
            },
            "2": {
                "summary": "Cuba",
                "value": {
                    "title": "Marina Resort Spa",
                    "location": "Varadero, Cuba",
                },
            },
        }
    ),
):
    added_hotel = await HotelService(db).hotel_add_service(hotel_data)
    return {"status": "Hotel added", "data": added_hotel}


@router.put("/{hotel_id}")
async def hotel_put(db: DBDep, hotel_id: int, hotel: HotelAdd):
    try:
        await HotelService(db).hotel_put_service(hotel_id, hotel)
    except ObjectNotFoundException:
        raise HTTPException(404, "Отель не найден")
    return {"message": "Данные об отеле изменены"}


@router.patch("/{hotel_id}")
async def hotel_patch(db: DBDep, hotel_id: int, hotel: HotelPatch):
    try:
        await HotelService(db).hotel_patch_service(hotel_id, hotel)
    except ObjectNotFoundException:
        raise HTTPException(404, "Отель не найден")
    return {"message": "Данные об отеле изменены"}


@router.delete("/{hotel_id}")
async def hotel_delete(db: DBDep, hotel_id: int):
    try:
        await HotelService(db).hotel_delete_service(hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(404, "Отель не найден")
    return {"message": "Отель удален"}
