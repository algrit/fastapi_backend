from fastapi import APIRouter, Body
from dependencies import PaginationDep

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
	{"id": 1, "title": "Sochi", "name": "sochi"},
	{"id": 2, "title": "Дубай", "name": "dubai"},
	{"id": 3, "title": "Мальдивы", "name": "maldivi"},
	{"id": 4, "title": "Геленджик", "name": "gelendzhik"},
	{"id": 5, "title": "Москва", "name": "moscow"},
	{"id": 6, "title": "Казань", "name": "kazan"},
	{"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


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
def add_hotel(title: str = Body(),
			  name: str = Body(),
			  ):
	new_hotel = dict(id=hotels[-1]["id"] + 1, title=title, name=name)
	hotels.append(new_hotel)
	return new_hotel


@router.put("/{hotel_id}")
def change_hotel_data(hotel_id: int,
					  new_title: str = Body(),
					  new_name: str = Body()
					  ):
	global hotels
	for hotel in hotels:
		if hotel["id"] == hotel_id:
			hotel["title"] = new_title
			hotel["name"] = new_name
			return hotel


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
