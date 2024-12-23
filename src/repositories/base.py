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

	async def get_one(self, **filter_by):
		query = select(self.model).filter_by(**filter_by)
		result = await self.session.execute(query)
		return result.scalars().one_or_none()

	async def add(self, data: BaseModel):
		add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
		result = await self.session.execute(add_data_stmt)
		return result.scalars().one()

	async def edit(self, data: BaseModel, **filter_by) -> None:
		edit_data_stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump())
		await self.session.execute(edit_data_stmt)


	async def delete(self, **filter_by) -> None:
		query = select(self.model).filter_by(**filter_by)
		obj_amount = len((await self.session.execute(query)).scalars().all())
		# obj_amount = len(obj_to_delete.scalars().all()))
		if obj_amount == 0:
			raise HTTPException(404, "No such object")
		elif obj_amount > 1:
			raise HTTPException(422, "Too much objects found")
		stmt = delete(self.model).filter_by(**filter_by)
		await self.session.execute(stmt)
