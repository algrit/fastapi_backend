import uvicorn
from fastapi import FastAPI, Body

app = FastAPI()

hotels = [
	{"id": 1, "title": "Sochi", "name": "name_Sochi"},
	{"id": 2, "title": "Dubai", "name": "name_Dubai"},
	{"id": 3, "title": "Sri-Lanka", "name": "name_Sri-Lanka"},
	{"id": 4, "title": "Afganistan", "name": "name_Afganistan"},
]


@app.put("/hotels/{hotel_id}")
def change_hotel_data(hotel_id: int,
					  new_title: str = Body(),
					  new_name: str = Body()):
	global hotels
	for hotel in hotels:
		if hotel["id"] == hotel_id:
			hotel["title"] = new_title
			hotel["name"] = new_name
			return hotel


@app.patch("/hotels/{hotel_id}")
def change_hotel_field(hotel_id: int,
					   new_title: str | None = Body(),
					   new_name: str | None = Body()):
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


if __name__ == "__main__":
	uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
