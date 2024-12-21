from sqlalchemy import select, insert, literal_column

from src.repositories.base import BaseRepository
from src.models.hotels import HotelsORM


class HotelsRepository(BaseRepository):
	model = HotelsORM

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
		return result.scalars().all()

	async def add(self, title, location):
		stmt = insert(HotelsORM).values(title=title, location=location)
		result = await self.session.execute(stmt)
		return result.last_inserted_params()