from typing import Annotated

from fastapi import Body
from pydantic import BaseModel


class Hotel(BaseModel):
	title: Annotated[str, Body()]
	name: Annotated[str, Body()]