from fastapi import APIRouter, Body
from sqlalchemy import insert, select

from src.models.hotels import HotelsORM
from src.schemas.hotels import Hotel
from src.api.dependencies import PaginationDep
from src.database import async_engine, async_session_maker

from src.repositories.hotels import HotelsRepository

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("",
			summary="Получить отели",
			description="Получить отели по ID, либо по полю 'title', либо все")
async def get_hotel(pagination: PaginationDep,
					title: str | None = None,
					location: str | None = None,
					):
	per_page = pagination.per_page or 5
	async with async_session_maker() as session:
		return await HotelsRepository(session).get_all(
			title=title,
			location=location,
			limit=per_page,
			offset=(pagination.page - 1) * per_page
		)


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
		added_object = await HotelsRepository(session).add(title=hotel.title, location=hotel.location)
		await session.commit()
		# return {"message": "insertion in DB complete correctly"}
		return {"status": "OK", "data": added_object}


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
