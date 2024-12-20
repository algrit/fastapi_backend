from fastapi import APIRouter, Body
from sqlalchemy import insert, select

from src.models.hotels import HotelsORM
from src.schemas.hotels import Hotel
from src.api.dependencies import PaginationDep
from src.database import async_engine, async_session_maker

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("",
			summary="Получить отели",
			description="Получить отели по ID, либо по полю 'title', либо все")
def get_hotel(pagination: PaginationDep,
			  id: int | None = None,
			  title: str | None = None,
			  ):
	if id:
		return [hotel for hotel in hotels if hotel["id"] == id]
	elif title:
		return [hotel for hotel in hotels if hotel["title"] == title]
	else:
		start_hotel_number = (pagination.page - 1) * pagination.per_page
		return hotels[start_hotel_number:][:start_hotel_number + pagination.per_page]


@router.post("",
			 summary="Добавить отель")
async def add_hotel(hotel: Hotel = Body(openapi_examples={
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
	async with async_session_maker() as session:
		stmt = insert(HotelsORM).values(**hotel.model_dump())
		# print(stmt.compile(async_engine, compile_kwargs={"literal_binds": True}))
		await session.execute(stmt)
		await session.commit()
	return {"message": "insertion in DB complete correctly"}


@router.put("/{hotel_id}")
def change_hotel_data(hotel_id: int, hotel: Hotel):
	global hotels
	for hotel_ in hotels:
		if hotel_["id"] == hotel_id:
			hotel_["title"] = hotel.title
			hotel_["name"] = hotel.name
			return hotel_


@router.patch("/{hotel_id}")
def change_hotel_field(hotel_id: int,
					   new_title: str | None = Body(),
					   new_name: str | None = Body()
					   ):
	if not new_title and not new_name:
		return {"message": "no new data"}
	global hotels
	for hotel in hotels:
		if hotel["id"] == hotel_id:
			if new_title:
				hotel["title"] = new_title
			if new_name:
				hotel["name"] = new_name
			return hotel
