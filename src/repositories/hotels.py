from sqlalchemy import select, insert, literal_column

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.utils import get_rooms_ids_to_book
from src.models.hotels import HotelsORM
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
	model = HotelsORM
	schema = Hotel

	async def get_hotels_by_date(
			self,
			date_from,
			date_to,
			title,
			location,
			limit,
			offset):
		rooms_ids_to_book = await get_rooms_ids_to_book(date_from, date_to)
		hotels_ids_to_book = select(RoomsOrm.hotel_id).filter(RoomsOrm.id.in_(rooms_ids_to_book))
		hotel_filters = [HotelsORM.id.in_(hotels_ids_to_book)]
		if title:
			hotel_filters.append(HotelsORM.title.contains(title))
		if location:
			hotel_filters.append(HotelsORM.location.contains(location))
		return await self.get_filtered(*hotel_filters, limit=limit, offset=offset)


