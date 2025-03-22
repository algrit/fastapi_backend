from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import NoFreeRoomsException, WrongDatesException, ObjectNotFoundException
from src.schemas.bookings import BookingAddRequest
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("", summary="Забронировать номер в отеле")
async def booking_add(db: DBDep, user_id: UserIdDep, data: BookingAddRequest):
    try:
        added_booking = await BookingService(db).booking_add_service(user_id, data)
    except WrongDatesException as exc:
        raise HTTPException(422, exc.detail)
    except NoFreeRoomsException as exc:
        raise HTTPException(409, exc.detail)
    except ObjectNotFoundException:
        raise HTTPException(404, "Номер не найден")
    return {"status": "Booking added", "data": added_booking}


@router.get("/me", summary="Получить мое бронирование")
async def bookings_get_mine(db: DBDep, user_id: UserIdDep):
    return await BookingService(db).bookings_get_mine_service(user_id)


@router.delete("/me/delete/{booking_id}", summary="Отменить мое бронирование")
async def booking_delete(db: DBDep, user_id: UserIdDep, booking_id: int):
    try:
        await BookingService(db).booking_delete_service(user_id, booking_id)
    except ObjectNotFoundException:
        raise HTTPException(404, "Бронирование не найдено")
    return {"status": "deleted"}
