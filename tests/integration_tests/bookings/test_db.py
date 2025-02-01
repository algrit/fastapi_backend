from datetime import date

from src.schemas.bookings import BookingAdd


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    added_booking = await db.bookings.add_one(BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2024, month=12, day=16),
        date_to=date(year=2025, month=2, day=9),
        price=100
    ))
    found_booking = await db.bookings.get_one(id=added_booking.id)
    assert added_booking == found_booking

    booking_to_edit = found_booking
    booking_to_edit.price = 200
    await db.bookings.edit(booking_to_edit, id=added_booking.id)
    edited_booking = await db.bookings.get_one(id=found_booking.id)
    assert edited_booking.price == 200

    await db.bookings.delete(id=found_booking.id)
    deleted_booking = await db.bookings.get_one(id=found_booking.id)
    assert not deleted_booking

    await db.commit()
