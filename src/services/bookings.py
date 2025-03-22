from src.api.dependencies import UserIdDep
from src.exceptions import ObjectNotFoundException
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.services.base import BaseService
from src.services.utils import DateChecker


class BookingService(BaseService, DateChecker):
    async def booking_add_service(self, user_id: UserIdDep, data: BookingAddRequest):
        DateChecker.date_check(data.date_from, data.date_to)
        room = await self.db.rooms.get_one(id=data.room_id)
        if room is None:
            raise ObjectNotFoundException
        booking = BookingAdd(user_id=user_id, price=room.price, **data.model_dump())
        added_booking = await self.db.bookings.add_booking(booking)
        await self.db.commit()
        return added_booking

    async def bookings_get_mine_service(self, user_id: UserIdDep):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def booking_delete_service(self, user_id: UserIdDep, booking_id: int):
        await self.db.bookings.delete(user_id=user_id, id=booking_id)
        await self.db.commit()
