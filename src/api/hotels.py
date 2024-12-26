from fastapi import APIRouter, Body

from src.schemas.hotels import HotelPatch, HotelAdd
from src.api.dependencies import PaginationDep, DBDep

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("",
            summary="Получить отели",
            description="Получить отели по полю 'title', либо 'location', либо все")
async def hotels_get(db: DBDep,
                     pagination: PaginationDep,
                     title: str | None = None,
                     location: str | None = None,
                     ):
    per_page = pagination.per_page or 5
    return await db.hotels.get_all(
        title=title,
        location=location,
        limit=per_page,
        offset=(pagination.page - 1) * per_page
    )


@router.get("/{hotel_id}", summary="Получить отель по ID")
async def hotel_get_by_id(db: DBDep, hotel_id: int):
    return await db.hotels.get_one(id=hotel_id)


@router.post("",
             summary="Добавить отель")
async def hotel_add(db: DBDep,
                    hotel_data: HotelAdd = Body(openapi_examples={
                        "1": {
                            "summary": "Rome",
                            "value": {
                                "title": "Coliseum Five Stars",
                                "location": "Rome, Italy",
                            }
                        },
                        "2": {
                            "summary": "Cuba",
                            "value": {
                                "title": "Marina Resort Spa",
                                "location": "Varadero, Cuba",
                            }
                        }
                    })):
    added_hotel = await db.hotels.add_one(hotel_data)
    return {"status": "OK", "data": added_hotel}


@router.put("/{hotel_id}")
async def hotel_put(db: DBDep,
                    hotel_id: int,
                    hotel: HotelAdd):
    await db.hotels.edit(hotel, id=hotel_id)
    return {"message": "OK"}


@router.patch("/{hotel_id}")
async def hotel_patch(db: DBDep,
                      hotel_id: int,
                      hotel: HotelPatch):
    await db.hotels.edit(hotel, exclude_unset=True, id=hotel_id)
    return {"message": "OK"}


@router.delete("/{hotel_id}")
async def hotel_delete(db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    return {"message": "OK"}
