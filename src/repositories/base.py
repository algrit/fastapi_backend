from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError

from src.exceptions import ObjectNotFoundException, UniquenessViolationException, ForeignKeyViolationException


class BaseRepository:
    model = None
    mapper = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(
            self, *filter, limit: int | None = None, offset: int | None = None, **filter_by
    ):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        if limit:
            query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self):
        return await self.get_filtered()

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def add_one(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        try:
            result = await self.session.execute(add_data_stmt)
        except IntegrityError as exc:
            if isinstance(exc.orig.__cause__, UniqueViolationError):
                raise UniquenessViolationException from exc
            elif isinstance(exc.orig.__cause__, ForeignKeyViolationError):
                raise ForeignKeyViolationException from exc
            else:
                raise exc
        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)

    async def add_bulk(self, data: list[BaseModel]):
        add_data_stmt = insert(self.model).values([schema.model_dump() for schema in data])
        try:
            await self.session.execute(add_data_stmt)
        except IntegrityError as exc:
            if isinstance(exc.orig.__cause__, UniqueViolationError):
                raise UniquenessViolationException from exc
            elif isinstance(exc.orig.__cause__, ForeignKeyViolationError):
                raise ForeignKeyViolationException from exc
            else:
                raise exc

    async def edit(self, data: BaseModel, exclude_unset=False, **filter_by) -> None:
        model = await self.get_one(**filter_by)
        if not model:
            raise ObjectNotFoundException
        edit_data_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(edit_data_stmt)

    async def delete(self, **filter_by) -> None:
        query = select(self.model).filter_by(**filter_by)
        obj_amount = len((await self.session.execute(query)).scalars().all())
        if obj_amount == 0:
            raise ObjectNotFoundException
        stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt)
