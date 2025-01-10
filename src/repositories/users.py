from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.users import UsersORM
from src.repositories.mappers.mappers import UserDataMapper, UserWithHashedPassDataMapper


class UsersRepository(BaseRepository):
    model = UsersORM
    mapper = UserDataMapper

    async def get_user_with_hashed_pass(self, email):
        query = select(UsersORM).filter_by(email=email)
        result = await self.session.execute(query)
        user = result.scalars().one_or_none()
        if user is None:
            return None
        return UserWithHashedPassDataMapper.map_to_domain_entity(user)
