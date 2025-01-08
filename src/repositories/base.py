from fastapi import HTTPException

from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import CompileError
from pydantic import BaseModel


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, limit: int | None = None, offset: int | None = None, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        if limit:
            query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

    async def get_all(self):
        return await self.get_filtered()

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model, from_attributes=True)

    async def add_one(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)

    async def add_bulk(self, data: list[BaseModel]):
        add_data_stmt = insert(self.model).values([schema.model_dump() for schema in data])
        await self.session.execute(add_data_stmt)

    async def edit(self, data: BaseModel, exclude_unset=False, **filter_by) -> None:
        edit_data_stmt = (update(self.model)
                          .filter_by(**filter_by)
                          .values(**data.model_dump(exclude_unset=exclude_unset)))
        try:
            await self.session.execute(edit_data_stmt)
        except CompileError:
            pass


    async def delete(self, **filter_by) -> None:
        query = select(self.model).filter_by(**filter_by)
        obj_amount = len((await self.session.execute(query)).scalars().all())
        if obj_amount == 0:
            raise HTTPException(404, "No such object")
        elif obj_amount > 1:
            raise HTTPException(422, "Too much objects found")
        stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt)
