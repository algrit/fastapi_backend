from datetime import datetime, timezone, timedelta

import bcrypt
import jwt

from src.config import settings
from src.exceptions import ObjectNotFoundException, WrongPassword, WrongAccessKey
from src.schemas.users import UserAddRequest, UserAdd
from src.services.base import BaseService


class AuthService(BaseService):
    @staticmethod
    def hash_password(raw_password):
        password = bytes(raw_password, "utf-8")
        return bcrypt.hashpw(password, bcrypt.gensalt(12))

    @staticmethod
    def verify_password(plain_password, hashed_password):
        password = bytes(plain_password, "utf-8")
        hashed = bytes(hashed_password, "utf-8")
        return bcrypt.checkpw(password, hashed)

    @staticmethod
    def create_jwt_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def decode_jwt_token(encoded_jwt):
        try:
            data = jwt.decode(
                encoded_jwt, key=settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
        except jwt.exceptions.InvalidSignatureError:
            raise WrongAccessKey
        return data["id"]

    async def register_user_service(self, data: UserAddRequest):
        hashed_password = self.hash_password(data.password)
        new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
        new_user = await self.db.users.add_one(new_user_data)
        await self.db.commit()
        return new_user

    async def login_service(self, data: UserAddRequest):
        user = await self.db.users.get_user_with_hashed_pass(email=data.email)
        if not user:
            raise ObjectNotFoundException
        if not self.verify_password(data.password, user.hashed_password):
            raise WrongPassword
        access_token = self.create_jwt_token({"id": user.id})
        return access_token

    async def get_me_service(self, user_id: int):
        return await self.db.users.get_one(id=user_id)
