from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import NoFreeRoomsException
from src.schemas.bookings import BookingAddRequest, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("", summary="Забронировать номер в отеле")
async def booking_add(db: DBDep, user_id: UserIdDep, data: BookingAddRequest):
    room = await db.rooms.get_one(id=data.room_id)
    booking = BookingAdd(user_id=user_id, price=room.price, **data.model_dump())
    try:
        added_booking = await db.bookings.add_booking(booking)
    except NoFreeRoomsException:
        raise HTTPException(400, "Can't book this room. No free rooms for these dates")
    await db.commit()
    return {"status": "OK", "data": added_booking}


@router.get("", summary="Получить все бронирования")
async def bookings_get_all(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me", summary="Получить мое бронирование")
async def bookings_get_mine(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.delete("/me/delete/{booking_id}", summary="Отменить мое бронирование")
async def booking_delete(db: DBDep, user_id: UserIdDep, booking_id: int):
    await db.bookings.delete(user_id=user_id, id=booking_id)
    await db.commit()
    return {"status": "deleted"}
