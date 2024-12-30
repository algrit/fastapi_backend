from sqlalchemy import select, func

from src.database import async_engine
from src.models.bookings import BookingsORM
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.schemas.rooms import Room, RoomAdd


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    # async def get_all(self,
    #                   hotel_id,
    #                   title,
    #                   description,
    #                   price,
    #                   quantity,
    #                   ):
    #     query = select(RoomsOrm)
    #     if hotel_id:
    #         query = query.filter_by(hotel_id=hotel_id)
    #     if title:
    #         query = query.filter(RoomsOrm.title.contains(title))
    #     if description:
    #         query = query.filter(RoomsOrm.description.contains(description))
    #     if price:
    #         query = query.filter(RoomsOrm.price.__le__(price))
    #     rooms = await self.session.execute(query)
    #     return [Room.model_validate(room, from_attributes=True) for room in rooms.scalars().all()]

    async def get_rooms_by_date(self, hotel_id, date_from, date_to):
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
        booked_rooms_cte = (
            select(BookingsORM.room_id, func.count("*").label("booked_rooms_count"))
            .select_from(BookingsORM)
            .filter(BookingsORM.date_from <= date_to, BookingsORM.date_to >= date_from)
            .group_by(BookingsORM.room_id)
            .cte(name="booked_rooms")
        )
        rooms_left_cte = (
            select(
                RoomsOrm.id.label("room_id"),
                (RoomsOrm.quantity - func.coalesce(booked_rooms_cte.c.booked_rooms_count, 0)).label("rooms_left"))
            .select_from(RoomsOrm)
            .outerjoin(booked_rooms_cte)
            .cte(name="rooms_left_table")
        )
        hotel_filtered_rooms = (
            select(RoomsOrm.id)
            .select_from(RoomsOrm)
            .filter_by(hotel_id=hotel_id)
            # .subquery(name="hotel_filter_subq")
        )
        rooms_ids = (
            select(rooms_left_cte.c.room_id)
            .filter(
                rooms_left_cte.c.rooms_left > 0,
                rooms_left_cte.c.room_id.in_(hotel_filtered_rooms),
            )
        )

        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids))
