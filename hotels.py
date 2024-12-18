from typing import Optional

from fastapi import APIRouter, Body

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels: list = [
	{"id": 1, "title": "Sochi", "name": "name_Sochi"},
	{"id": 2, "title": "Dubai", "name": "name_Dubai"},
	{"id": 3, "title": "Sri-Lanka", "name": "name_Sri-Lanka"},
	{"id": 4, "title": "Afghanistan", "name": "name_Afghanistan"},
]


@router.get("",
			summary="Получить отели",
			description="Получить отели по ID, либо по полю 'title', либо все")
def get_hotel(id: int | None = None,
			  title: str | None = None ,
			  ):
	if id:
		return [hotel for hotel in hotels if hotel["id"] == id]
	elif title:
		return [hotel for hotel in hotels if hotel["title"] == title]
	else:
		return hotels


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
