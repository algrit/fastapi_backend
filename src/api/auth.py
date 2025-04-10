from fastapi import APIRouter, HTTPException, Response, Body

from src.exceptions import (
    UniquenessViolationException,
    ObjectNotFoundException,
    WrongPassword,
    WrongAccessKey,
)
from src.schemas.users import UserAddRequest
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep, DBDep

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(data: UserAddRequest, db: DBDep):
    try:
        new_user = await AuthService(db).register_user_service(data)
    except UniquenessViolationException:
        raise HTTPException(
            409, "Пользователь с такой почтой уже существует. Используйте другую почту"
        )
    return {"status": "User added", "data": new_user}


@router.post("/login")
async def login(
    db: DBDep,
    response: Response,
    data: UserAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "algri",
                "value": {
                    "email": "algri@example.com",
                    "password": "1234",
                },
            },
            "2": {
                "summary": "mama",
                "value": {
                    "email": "mama@example.com",
                    "password": "фисву",
                },
            },
        }
    ),
):
    try:
        access_token = await AuthService(db).login_service(data)
    except ObjectNotFoundException:
        raise HTTPException(404, "Нет такого пользователя")
    except WrongPassword as exc:
        raise HTTPException(403, exc.detail)
    response.set_cookie(key="access_token", value=access_token)
    return {"access_token": access_token}


@router.get("/me", summary="Получить данные текущего пользователя")
async def get_me(db: DBDep, user_id: UserIdDep):
    try:
        me = await AuthService(db).get_me_service(user_id)
    except WrongAccessKey as exc:
        raise HTTPException(403, exc.detail)
    return me


@router.get("/logout", summary="Выйти из системы")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "OK"}
