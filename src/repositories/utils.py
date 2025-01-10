from datetime import date
from sqlalchemy import select, func

from src.models.bookings import BookingsORM
from src.models.rooms import RoomsORM


def get_rooms_ids_to_book(date_from: date, date_to: date, hotel_id: int | None = None):
    booked_rooms_cte = (
        select(BookingsORM.room_id, func.count("*").label("booked_rooms_count"))
        .select_from(BookingsORM)
        .filter(BookingsORM.date_from <= date_to, BookingsORM.date_to >= date_from)
        .group_by(BookingsORM.room_id)
        .cte(name="booked_rooms")
    )
    rooms_left_cte = (
        select(
            RoomsORM.id.label("room_id"),
            (RoomsORM.quantity - func.coalesce(booked_rooms_cte.c.booked_rooms_count, 0)).label("rooms_left"))
        .select_from(RoomsORM)
        .outerjoin(booked_rooms_cte)
        .cte(name="rooms_left_table")
    )
    hotel_filtered_rooms = (
        select(RoomsORM.id)
        .select_from(RoomsORM)
    )
    if hotel_id is not None:
        hotel_filtered_rooms = hotel_filtered_rooms.filter_by(hotel_id=hotel_id)

    rooms_ids = (
        select(rooms_left_cte.c.room_id)
        .filter(
            rooms_left_cte.c.rooms_left > 0,
            rooms_left_cte.c.room_id.in_(hotel_filtered_rooms),
        )
    )

    return rooms_ids
