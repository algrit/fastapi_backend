from fastapi import APIRouter, HTTPException, Response, Body

from src.exceptions import UniquenessViolationException, ObjectNotFoundException, WrongPassword
from src.schemas.users import UserAddRequest, UserAdd
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep, DBDep

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(data: UserAddRequest, db: DBDep):
    try:
        new_user = AuthService(db).register_user_service(data)
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
        access_token = AuthService(db).login_service(data)
    except ObjectNotFoundException:
        raise HTTPException(404, "Нет такого пользователя")
    except WrongPassword as exc:
        raise HTTPException(403, exc.detail)
    response.set_cookie(key="access_token", value=access_token)
    return {"access_token": access_token}


@router.get("/me", summary="Получить ID текущего пользователя")
async def get_me(db: DBDep, user_id: UserIdDep):
    return await db.users.get_one(id=user_id)


@router.get("/logout", summary="Выйти из системы")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "OK"}
