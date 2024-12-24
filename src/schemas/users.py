from typing import Annotated
from fastapi import Body
from pydantic import BaseModel, EmailStr


class UserAddRequest(BaseModel):
	email: Annotated[EmailStr, Body()]
	password: Annotated[str, Body()]


class UserAdd(BaseModel):
	email: Annotated[EmailStr, Body()]
	hashed_password: str


class User(UserAdd):
	id: int