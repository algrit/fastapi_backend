from fastapi import APIRouter, Body

from src.schemas.rooms import RoomAddRequest, RoomAdd, RoomPatch
from src.api.dependencies import DBDep

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def rooms_get(
        db: DBDep,
        hotel_id: int,
        title: str | None = None,
        description: str | None = None,
        price: int | None = None,
        quantity: int | None = None,
):
    return await db.rooms.get_all(
        hotel_id=hotel_id,
        title=title,
        description=description,
        price=price,
        quantity=quantity,
    )


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить номер по ИД отеля и номера")
async def room_get_by_id(db: DBDep, hotel_id: int, room_id: int):
    return await db.rooms.get_one(hotel_id=hotel_id, room_id=room_id)


@router.post("/{hotel_id}/rooms", summary="Добавить номера в отель")
async def room_add(db: DBDep,
                   hotel_id: int,
                   data: RoomAddRequest = Body(openapi_examples={
                       "1": {
                           "summary": "Luxe",
                           "value": {
                               "title": "Double Luxe",
                               "description": "Very cool fancy room",
                               "price": 100500,
                               "quantity": 1,
                           }
                       },
                       "2": {
                           "summary": "Очередняра",
                           "value": {
                               "title": "Койка и туалет",
                               "description": "Душ общий на этаж",
                               "price": 15,
                               "quantity": 80,
                           }
                       }
                   })):
    data_with_hotel = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    added_room = await db.rooms.add_one(data_with_hotel)
    await db.commit()
    return {"status": "OK", "data": added_room}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Изменить все данные комнаты")
async def room_put(db: DBDep,
                   hotel_id: int,
                   room_id: int,
                   data: RoomAddRequest):
    await db.rooms.edit(data, hotel_id=hotel_id, room_id=room_id)
    await db.commit()
    return {"message": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Изменить некоторые данные комнаты")
async def room_patch(db: DBDep,
                     hotel_id: int,
                     room_id: int,
                     data: RoomPatch
                     ):
    await db.rooms.edit(data, exclude_unset=True, hotel_id=hotel_id, room_id=room_id)
    await db.commit()
    return {"message": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удалить номер")
async def room_delete(db: DBDep,
                      hotel_id: int,
                      room_id: int):
    filter_by = {"hotel_id": hotel_id, "id": room_id}
    await db.rooms.delete(**filter_by)
    await db.commit()
    return {"message": "OK"}
