from datetime import date
from sqlalchemy import select
from fastapi import HTTPException

from src.models.bookings import BookingsORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import get_rooms_ids_to_book
from src.schemas.bookings import BookingAdd


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = select(BookingsORM).filter(BookingsORM.date_from == date.today())
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in res.scalars().all()]

    async def add_booking(self, booking: BookingAdd):
        room_id = booking.room_id
        query = get_rooms_ids_to_book(date_from=booking.date_from, date_to=booking.date_to)
        rooms_ids_to_book = (await self.session.execute(query)).scalars().all()
        if room_id not in rooms_ids_to_book:
            raise HTTPException(400, "Can't book this room. No free rooms for these dates")
        else:
            return await self.add_one(booking)
