from typing import Annotated
from fastapi import APIRouter, Body

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/room")
async def get_room(
        hotel_id: int,
        title: str | None = None,
        description: str | None = None,
        price: int | None = None,
        quantity: int | None = None,
):
    async with async_session_maker() as session:
        rooms = await RoomsRepository(session).get_all(
            hotel_id=hotel_id,
            title=title,
            description=description,
            price=price,
            quantity=quantity,
        )
    return rooms


@router.post("/{hotel_id}/room", summary="Добавить номера в отель")
async def add_room(hotel_id: int,
                   data: RoomAdd = Body(openapi_examples={
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
    async with async_session_maker() as session:
        added_room = await RoomsRepository(session).add_one(room_dict)
        await session.commit()
    return added_room
