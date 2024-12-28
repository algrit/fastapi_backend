from sqlalchemy import select, insert

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.schemas.rooms import Room, RoomAdd


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_all(self,
                      hotel_id,
                      title,
                      description,
                      price,
                      quantity,
                      ):
        query = select(RoomsOrm)
        if hotel_id:
            query = query.filter_by(hotel_id=hotel_id)
        if title:
            query = query.filter(RoomsOrm.title.contains(title))
        if description:
            query = query.filter(RoomsOrm.description.contains(description))
        if price:
            query = query.filter(RoomsOrm.price.__le__(price))
        rooms = await self.session.execute(query)
        return [Room.model_validate(room, from_attributes=True) for room in rooms.scalars().all()]


    async def get_rooms_by_date(self, date_from, date_to):
        """
        with booked_rooms as (
            select room_id, count(*) as booked_rooms_count
            from bookings b
            where date_from <= '2024-12-30' and date_to >= '2024-12-20'
            group by room_id ),

        rooms_left_table as (
            select r.id, r.quantity - coalesce(booked_rooms.booked_rooms_count, 0) as rooms_left
            from rooms r
            left join booked_rooms on r.id = booked_rooms.room_id)

        select * from rooms_left_table
        where rooms_left > 0
        """
        pass