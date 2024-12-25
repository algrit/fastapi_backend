from sqlalchemy import select, insert, literal_column

from src.repositories.base import BaseRepository
from src.models.hotels import HotelsORM
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
	model = HotelsORM
	schema = Hotel

	async def get_all(
			self,
			title,
			location,
			limit,
			offset):
		query = select(HotelsORM)
		if title:
			query = query.filter(HotelsORM.title.contains(title))
		if location:
			query = query.filter(HotelsORM.location.contains(location))
		query = (query
				 .limit(limit)
				 .offset(offset)
				 )
		result = await self.session.execute(query)
		return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]