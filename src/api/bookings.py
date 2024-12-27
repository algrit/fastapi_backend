from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("", summary="Забронировать номер в отеле")
async def booking_add(db: DBDep,
                      user_id: UserIdDep,
                      data: BookingAddRequest):
    room = await db.rooms.get_one(id=data.room_id)
    booking = BookingAdd(user_id=user_id, price=room.price, **data.model_dump())
    added_booking = await db.bookings.add_one(booking)
    await db.commit()
    return {"status": "OK", "data": added_booking}


@router.get("", summary="Получить все бронирования")
async def bookings_get_all(db: DBDep):
    return await db.bookings.get_all()