from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.repositories.mappers.mappers import RoomDataMapper, RoomWithRelsDataMapper
from src.repositories.utils import get_rooms_ids_to_book


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDataMapper

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
        return RoomWithRelsDataMapper.map_to_domain_entity(model)

    async def get_rooms_by_date(self, hotel_id, date_from, date_to):
        rooms_ids_to_book = get_rooms_ids_to_book(date_from, date_to, hotel_id)
        query = (
            select(RoomsOrm)
            .options(selectinload(RoomsOrm.features))
            .filter(RoomsOrm.id.in_(rooms_ids_to_book)))
        result = await self.session.execute(query)
        return [RoomWithRelsDataMapper.map_to_domain_entity(model) for model in result.scalars().all()]
