from src.repositories.users import UsersRepository
from src.repositories.hotels import HotelsRepository
from src.repositories.rooms import RoomsRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UsersRepository(self.session)
        self.hotels = HotelsRepository(self.session)
        self.rooms = RoomsRepository(self.session)

    async def __aexit__(self, *args):
        self.session.rollback()
        self.session.close()

    async def commit(self):
        await self.session.commit()