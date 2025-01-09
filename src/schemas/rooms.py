from typing import Annotated

from pydantic import BaseModel, ConfigDict
from fastapi import Body


class RoomAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    features_ids: list[int] | list = []


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int


class Room(RoomAdd):
    id: int


class RoomPatchRequest(BaseModel):
    title: Annotated[str | None, Body(None)]
    description: Annotated[str | None, Body(None)]
    price: Annotated[int | None, Body(None)]
    quantity: Annotated[int | None, Body(None)]
    features_ids: Annotated[list[int] | None, Body(None)]


class RoomPatch(BaseModel):
    hotel_id: int
    title: Annotated[str | None, Body(None)]
    description: Annotated[str | None, Body(None)]
    price: Annotated[int | None, Body(None)]
    quantity: Annotated[int | None, Body(None)]
