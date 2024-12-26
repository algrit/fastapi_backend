from pydantic import BaseModel
# from sqlalchemy import


class RoomAdd(BaseModel):
	title: str
	description: str | None = None
	price: int
	quantity: int


class Room(RoomAdd):
	hotel_id: int
	id: int