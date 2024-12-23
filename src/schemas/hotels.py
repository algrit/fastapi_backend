from typing import Annotated

from fastapi import Body
from pydantic import BaseModel


class HotelAdd(BaseModel):
	title: Annotated[str, Body()]
	location: Annotated[str, Body()]


class Hotel(HotelAdd):
	id: int


class HotelPatch(BaseModel):
	title: Annotated[str | None, Body(None)]
	location: Annotated[str | None, Body(None)]