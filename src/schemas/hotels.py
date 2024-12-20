from typing import Annotated

from fastapi import Body
from pydantic import BaseModel


class Hotel(BaseModel):
	title: Annotated[str, Body()]
	location: Annotated[str, Body()]


class HotelPatch(BaseModel):
	title: Annotated[str | None, Body(None)]
	location: Annotated[str | None, Body(None)]