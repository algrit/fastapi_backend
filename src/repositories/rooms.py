from sqlalchemy import select, func

from src.repositories.utils import get_rooms_ids_to_book
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room


    async def get_rooms_by_date(self, hotel_id, date_from, date_to):
        rooms_ids_to_book = await get_rooms_ids_to_book(date_from, date_to, hotel_id)
        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_book))