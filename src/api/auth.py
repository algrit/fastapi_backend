from datetime import timedelta, timezone, datetime

from fastapi import APIRouter, HTTPException, Response, Request

from passlib.context import CryptContext
import jwt

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserAddRequest, UserAdd, User

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

JWT_SECRET_KEY = "24bc638d088b731a33aab0a5e1f989b4a384bfefc86a2741a94ace94ac197ca0"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta | None = None):
	to_encode = data.copy()
	expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
	return encoded_jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
	return pwd_context.verify(plain_password, hashed_password)


@router.post("/register")
async def register_user(data: UserAddRequest):
	hashed_password = pwd_context.hash(data.password)
	new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
	async with async_session_maker() as session:
		await UsersRepository(session).add(new_user_data)
		await session.commit()
	return {"message": "OK"}


@router.post("login")
async def login(data: UserAddRequest, response: Response):
	async with async_session_maker() as session:
		user = await UsersRepository(session).get_one(email=data.email)
		if not user:
			raise HTTPException(401, "Нет такого пользователя")
		if not verify_password(data.password, user.hashed_password):
			raise HTTPException(401, "Неверный пароль")
		access_token = create_access_token({"id": user.id})
		response.set_cookie(key="access_token", value=access_token)
	return {"access_token": access_token}
