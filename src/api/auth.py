from fastapi import APIRouter, HTTPException, Response, Depends

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserAddRequest, UserAdd, User
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(data: UserAddRequest):
	hashed_password = AuthService().hash_password(data.password)
	new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
	async with async_session_maker() as session:
		await UsersRepository(session).add_one(new_user_data)
		await session.commit()
	return {"message": "OK"}


@router.post("/login")
async def login(data: UserAddRequest, response: Response):
	async with async_session_maker() as session:
		user = await UsersRepository(session).get_user_with_hashed_pass(email=data.email)
		if not user:
			raise HTTPException(401, "Нет такого пользователя")
		if not AuthService().verify_password(data.password, user.hashed_password):
			raise HTTPException(401, "Неверный пароль")
		access_token = AuthService().create_jwt_token({"id": user.id})
		response.set_cookie(key="access_token", value=access_token)
	return {"access_token": access_token}


@router.get("/me", summary="Получить ID текущего пользователя")
async def get_me(user_id: UserIdDep):
	async with async_session_maker() as session:
		user = await UsersRepository(session).get_one(id=user_id)
	return user


@router.get("/logout", summary="Выйти из системы")
def logout(response: Response):
	response.delete_cookie(key="access_token")
	return {"message": "OK"}