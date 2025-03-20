from datetime import date
from fastapi import APIRouter, Body, Query, HTTPException

from src.schemas.rooms import RoomAddRequest, RoomPatchRequest
from src.api.dependencies import DBDep
from src.exceptions import (
    ObjectNotFoundException,
    WrongDatesException,
    ForeignKeyViolationException,
)
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получить свободные номера указанного отеля по дате")
async def rooms_get_by_date(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(default="2024-12-20"),
    date_to: date = Query(default="2024-12-30"),
):
    try:
        free_rooms = await RoomService(db).get_free_rooms_by_date_service(
            hotel_id, date_from, date_to
        )
    except WrongDatesException as exc:
        raise HTTPException(422, exc.detail)
    except ObjectNotFoundException:
        raise HTTPException(404, "Нет такого отеля")
    return {"free_rooms_for_these_dates": free_rooms}


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить номер по ИД отеля и номера")
async def room_get_by_id(db: DBDep, hotel_id: int, room_id: int):
    try:
        room = await RoomService(db).room_get_by_id_service(hotel_id, room_id)
    except ObjectNotFoundException:
        raise HTTPException(404, "В этом отеле нет такой комнаты")
    return room


@router.post("/{hotel_id}/rooms", summary="Добавить номера в отель")
async def room_add(
    db: DBDep,
    hotel_id: int,
    data: RoomAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Luxe",
                "value": {
                    "title": "Double Luxe",
                    "description": "Very cool fancy room",
                    "price": 100500,
                    "quantity": 1,
                },
            },
            "2": {
                "summary": "Очередняра",
                "value": {
                    "title": "Койка и туалет",
                    "description": "Душ общий на этаж",
                    "price": 15,
                    "quantity": 80,
                },
            },
            "3": {
                "summary": "Президенсткий",
                "value": {
                    "title": "PRESIDENT LUXE",
                    "description": "FANCY",
                    "price": 1000000,
                    "quantity": 1,
                    "features_ids": [2, 3],
                },
            },
        }
    ),
):
    try:
        added_room = await RoomService(db).room_add_service(hotel_id, data)
    except ObjectNotFoundException:
        raise HTTPException(404, "Нет такого отеля")
    except ForeignKeyViolationException:
        raise HTTPException(404, "В списке нет удобств с таким ID")
    return {"status": "Room added", "data": added_room}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Изменить все данные номера")
async def room_put(db: DBDep, hotel_id: int, room_id: int, data: RoomAddRequest):
    try:
        await RoomService(db).room_put_service(hotel_id, room_id, data)
    except ObjectNotFoundException:
        raise HTTPException(404, "В этом отеле нет такой комнаты")
    return {"message": "Данные о номере изменены"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Изменить некоторые данные номера")
async def room_patch(db: DBDep, hotel_id: int, room_id: int, data: RoomPatchRequest):
    try:
        await RoomService(db).room_patch_service(hotel_id, room_id, data)
    except ObjectNotFoundException:
        raise HTTPException(404, "В этом отеле нет такой комнаты")
    return {"message": "Данные о номере изменены"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удалить номер")
async def room_delete(db: DBDep, hotel_id: int, room_id: int):
    try:
        await RoomService(db).room_delete_service(hotel_id, room_id)
    except ObjectNotFoundException:
        raise HTTPException(404, "В этом отеле нет такой комнаты")
    return {"message": "Номер удален"}
