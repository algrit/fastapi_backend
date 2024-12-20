from sqlalchemy import select

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
