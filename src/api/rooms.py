from lib2to3.btm_utils import reduce_tree
from typing import Annotated
from fastapi import APIRouter

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
				   data: RoomAdd):
	async with async_session_maker() as session:
		print(data)
		added_room = await RoomsRepository(session).add_one(hotel_id=hotel_id, title=data.title, price=data.price, quantity=data.quantity)
		await session.commit()
		return added_room
