from typing import Annotated
from fastapi import APIRouter, Body

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAddRequest, RoomAdd, RoomPatch

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def rooms_get(
        hotel_id: int,
        title: str | None = None,
        description: str | None = None,
        price: int | None = None,
        quantity: int | None = None,
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            hotel_id=hotel_id,
            title=title,
            description=description,
            price=price,
            quantity=quantity,
        )

@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить номер по ИД отеля и номера")
async def room_get_by_id(hotel_id: int, room_id: int):
    filter_by = {"hotel_id": hotel_id, "id": room_id}
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one(**filter_by)


@router.post("/{hotel_id}/rooms", summary="Добавить номера в отель")
async def room_add(hotel_id: int,
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
    room_dict = {"hotel_id": hotel_id}
    room_dict.update(**data.model_dump())
    data_with_hotel = RoomAdd(**room_dict)
    async with async_session_maker() as session:
        added_room = await RoomsRepository(session).add_one(data_with_hotel)
        await session.commit()
    return {"status": "OK", "data": added_room}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Изменить все данные комнаты")
async def room_put(hotel_id: int,
                   room_id: int,
                   data: RoomAddRequest):
    filter_by = {"hotel_id": hotel_id, "id": room_id}
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(data, **filter_by)
        await session.commit()
    return {"message": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Изменить некоторые данные комнаты")
async def room_patch(hotel_id: int,
                     room_id: int,
                     data: RoomPatch
                     ):
    filter_by = {"hotel_id": hotel_id, "id": room_id}
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(data, exclude_unset=True, **filter_by)
        await session.commit()
    return {"message": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удалить номер")
async def room_delete(hotel_id: int, room_id: int):
    filter_by = {"hotel_id": hotel_id, "id": room_id}
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(**filter_by)
        await session.commit()
    return {"message": "OK"}