from sqlalchemy import select, insert
from pydantic import BaseModel
from src.database import Base


class BaseRepository:
	model = None

	def __init__(self, session):
		self.session = session

	async def get_all(self, **kwargs):
		query = select(self.model)
		result = await self.session.execute(query)
		return result.scalars().all()

	async def add(self, data: BaseModel):
		add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
		result = await self.session.execute(add_data_stmt)
		return result.scalars().one()
