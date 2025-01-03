from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext
import jwt

from src.config import settings


class AuthService:
	pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

	def hash_password(self, password):
		return self.pwd_context.hash(password)

	def verify_password(self, plain_password, hashed_password):
		return self.pwd_context.verify(plain_password, hashed_password)

	@staticmethod
	def create_jwt_token(data: dict) -> str:
		to_encode = data.copy()
		expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
		to_encode.update({"exp": expire})
		encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
		return encoded_jwt

	@staticmethod
	def decode_jwt_token(token: str) -> int:
		user_id = jwt.decode(token, key=settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM)["id"]
		return user_id