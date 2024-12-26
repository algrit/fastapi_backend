from fastapi import APIRouter, HTTPException, Response

from src.schemas.users import UserAddRequest, UserAdd
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep, DBDep

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(data: UserAddRequest, db: DBDep):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    await db.users.add_one(new_user_data)
    await db.commit()
    return {"message": "OK"}


@router.post("/login")
async def login(db: DBDep,
                data: UserAddRequest,
                response: Response):
    user = await db.users.get_user_with_hashed_pass(email=data.email)
    if not user:
        raise HTTPException(401, "Нет такого пользователя")
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(401, "Неверный пароль")
    access_token = AuthService().create_jwt_token({"id": user.id})
    response.set_cookie(key="access_token", value=access_token)
    return {"access_token": access_token}


@router.get("/me", summary="Получить ID текущего пользователя")
async def get_me(db: DBDep, user_id: UserIdDep):
    return await db.users.get_one(id=user_id)


@router.get("/logout", summary="Выйти из системы")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "OK"}
