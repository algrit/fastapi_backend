from sqlalchemy import select, insert


class BaseRepository:
	model = None

	def __init__(self, session):
		self.session = session

	async def get_all(self, **kwargs):
		query = select(self.model)
		result = await self.session.execute(query)
		return result.scalars().all()

	async def add(self, **kwargs):
		stmt = insert(self.model).values(**kwargs)
		result = await self.session.execute(stmt)
		return result