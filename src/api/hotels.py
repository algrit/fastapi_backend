from fastapi import APIRouter, Body

from src.schemas.hotels import HotelPatch, HotelAdd
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("",
			summary="Получить отели",
			description="Получить отели по полю 'title', либо 'location', либо все")
async def hotels_get(pagination: PaginationDep,
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


@router.get("/{hotel_id}", summary="Получить отель по ID")
async def hotel_get_by_id(hotel_id: int):
	async with async_session_maker() as session:
		hotel_obj = await HotelsRepository(session).get_one(id=hotel_id)
		return hotel_obj


@router.post("",
			 summary="Добавить отель")
async def hotel_add(hotel_data: HotelAdd = Body(openapi_examples={
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
		added_hotel = await HotelsRepository(session).add_one(hotel_data)
		await session.commit()
	# return {"message": "insertion in DB complete correctly"}
	return {"status": "OK", "data": added_hotel}


@router.put("/{hotel_id}")
async def hotel_put(hotel_id: int, hotel: HotelAdd):
	async with async_session_maker() as session:
		await HotelsRepository(session).edit(hotel, id=hotel_id)
		await session.commit()
		return {"message": "OK"}


@router.patch("/{hotel_id}")
async def hotel_patch(hotel_id: int, hotel: HotelPatch):
	async with async_session_maker() as session:
		await HotelsRepository(session).edit(hotel, exclude_unset=True, id=hotel_id)
		await session.commit()


@router.delete("/{hotel_id}")
async def hotel_delete(hotel_id: int):
	async with async_session_maker() as session:
		await HotelsRepository(session).delete(id=hotel_id)
		await session.commit()
		return {"message": "OK"}
