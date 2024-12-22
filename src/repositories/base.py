from fastapi import HTTPException

from sqlalchemy import select, insert, update, delete
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

	async def edit(self, id, data: BaseModel):
		edit_data_stmt = update(self.model).filter_by(id=id).values(**data.model_dump()).returning(self.model)
		result = await self.session.execute(edit_data_stmt)
		return result.scalars().one()

	async def delete(self, id: int):
		query = select(self.model).filter_by(id=id)
		obj_amount = len((await self.session.execute(query)).scalars().all())
		# obj_amount = len(obj_to_delete.scalars().all()))
		if obj_amount == 0:
			raise HTTPException(404, "No such object")
		elif obj_amount > 1:
			raise HTTPException(422, "Too much objects found")
		stmt = delete(self.model).filter_by(id=id).returning(self.model)
		result = await self.session.execute(stmt)
		return result.scalars().one()
