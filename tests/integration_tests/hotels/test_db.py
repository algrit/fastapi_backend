from src.schemas.hotels import HotelAdd


async def test_hotel_add(db):
    hotel_data = HotelAdd(title="Valmer Resort", location="Mahe, Seychellas")
    await db.hotels.add_one(hotel_data)
    await db.commit()
