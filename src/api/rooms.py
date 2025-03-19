from datetime import date
from fastapi import APIRouter, Body, Query, HTTPException

from src.schemas.features import RoomFeatureAdd
from src.schemas.rooms import RoomAddRequest, RoomAdd, RoomPatch, RoomPatchRequest
from src.api.dependencies import DBDep
from src.exceptions import DBException, ObjectNotFoundException

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def rooms_get_by_date(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(examples=["2024-12-20"]),
    date_to: date = Query(examples=["2024-12-30"]),
):
    if date_from >= date_to:
        raise HTTPException(409, "'Date to' must be bigger than 'Date from'")
    return await db.rooms.get_rooms_by_date(hotel_id, date_from, date_to)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить номер по ИД отеля и номера")
async def room_get_by_id(db: DBDep, hotel_id: int, room_id: int):
    room = await db.rooms.get_one(hotel_id=hotel_id, id=room_id)
    if room:
        return room
    raise HTTPException(404, "No room with such ID")


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
    data_with_hotel = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    try:
        added_room = await db.rooms.add_one(data_with_hotel)
    except DBException:
        raise HTTPException(409, "No such hotel")
    if data.features_ids:
        features_list = [
            RoomFeatureAdd(room_id=added_room.id, feature_id=f_id) for f_id in data.features_ids
        ]
        await db.room_features.add_bulk(features_list)
    await db.commit()
    return {"status": "OK", "data": added_room}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Изменить все данные комнаты")
async def room_put(db: DBDep, hotel_id: int, room_id: int, data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    try:
        await db.rooms.edit(_room_data, id=room_id)
    except ObjectNotFoundException:
        raise HTTPException(404, "Room not found")
    await db.room_features.update_rooms_features(room_id, data.features_ids)
    await db.commit()
    return {"message": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Изменить некоторые данные комнаты")
async def room_patch(db: DBDep, hotel_id: int, room_id: int, data: RoomPatchRequest):
    if any([data.title, data.description, data.price, data.quantity]):
        _room_data = RoomPatch(hotel_id=hotel_id, **data.model_dump(exclude_unset=True))
        try:
            await db.rooms.edit(_room_data, exclude_unset=True, id=room_id)
        except ObjectNotFoundException:
            raise HTTPException(404, "Room not found")
    if getattr(data, "features_ids", None):
        await db.room_features.update_rooms_features(room_id, data.features_ids)
    await db.commit()
    return {"message": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удалить номер")
async def room_delete(db: DBDep, hotel_id: int, room_id: int):
    filter_by = {"hotel_id": hotel_id, "id": room_id}
    try:
        await db.rooms.delete(**filter_by)
    except ObjectNotFoundException:
        raise HTTPException(404, "Room not found")
    await db.commit()
    return {"message": "OK"}
