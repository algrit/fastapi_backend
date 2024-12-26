from typing import Annotated

from pydantic import BaseModel
from fastapi import Body


class RoomAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int


class RoomAdd(RoomAddRequest):
    hotel_id: int


class Room(RoomAdd):
    id: int


class RoomPatch(BaseModel):
    title: Annotated[str | None, Body(None)]
    description: Annotated[str | None, Body(None)]
    price: Annotated[int | None, Body(None)]
    quantity: Annotated[int | None, Body(None)]
