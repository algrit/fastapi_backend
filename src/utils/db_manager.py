from src.repositories.users import UsersRepository
from src.repositories.hotels import HotelsRepository
from src.repositories.rooms import RoomsRepository
from src.repositories.bookings import BookingsRepository
from src.repositories.features import FeaturesRepository, RoomsFeaturesRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UsersRepository(self.session)
        self.hotels = HotelsRepository(self.session)
        self.rooms = RoomsRepository(self.session)
        self.bookings = BookingsRepository(self.session)
        self.features = FeaturesRepository(self.session)
        self.room_features = RoomsFeaturesRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
