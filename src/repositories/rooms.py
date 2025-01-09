from sqlalchemy import select, func
from sqlalchemy.orm import selectinload, joinedload

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.repositories.utils import get_rooms_ids_to_book
from src.schemas.rooms import Room, RoomWithRels


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_one(self, **filter_by):
        query = (
            select(RoomsOrm)
            .options(selectinload(RoomsOrm.features))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return RoomWithRels.model_validate(model, from_attributes=True)

    async def get_rooms_by_date(self, hotel_id, date_from, date_to):
        rooms_ids_to_book = get_rooms_ids_to_book(date_from, date_to, hotel_id)
        query = (
            select(RoomsOrm)
            .options(selectinload(RoomsOrm.features))
            .filter(RoomsOrm.id.in_(rooms_ids_to_book)))
        result = await self.session.execute(query)
        return [RoomWithRels.model_validate(model, from_attributes=True) for model in result.scalars().all()]
