from pydantic import BaseModel


class RoomAdd(BaseModel):
	title: str
	description: str | None = None
	price: int
	quantity: int


class Room(RoomAdd):
	hotel_id: int
	id: int