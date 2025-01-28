from src.database import async_session_maker_null_pool
from src.schemas.hotels import HotelAdd
from src.utils.db_manager import DBManager


async def test_hotel_add():
    hotel_data = HotelAdd(title="Valmer Resort", location="Mahe, Seychellas")
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.hotels.add_one(hotel_data)
        await db.commit()
