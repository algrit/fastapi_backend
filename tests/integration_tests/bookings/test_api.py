import pytest


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
	(1, "2025-03-10", "2025-03-20", 200),
	(1, "2025-03-10", "2025-03-20", 400),
	(1, "2025-03-02", "2025-03-05", 200),
])
async def test_booking_add(db, authenticated_ac, room_id, date_from, date_to, status_code):
	booking_json = {"room_id": room_id, "date_from": date_from, "date_to": date_to}
	response = await authenticated_ac.post("/bookings", json=booking_json)

	assert response.status_code == status_code
	if status_code == 200:
		res = response.json()
		assert res["data"]["id"]


@pytest.fixture(scope="function", autouse=False)
async def clean_bookings(db, authenticated_ac):
	response = await authenticated_ac.get("/bookings/me")
	for booking in response.json():
		print(booking)
		response = await authenticated_ac.delete(f"/bookings/me/delete/{booking['id']}")
		assert response.status_code == 200


@pytest.mark.parametrize("room_id, date_from, date_to, status_code, bookings_count", [
	(1, "2025-03-10", "2025-03-20", 200, 1),
	(1, "2025-03-10", "2025-03-20", 200, 1),
	(1, "2025-03-02", "2025-03-05", 200, 1),
])
async def test_add_and_get_bookings(db, authenticated_ac, clean_bookings, room_id, date_from, date_to, status_code,
                                    bookings_count):
	booking_json = {"room_id": room_id, "date_from": date_from, "date_to": date_to}
	add_response = await authenticated_ac.post("/bookings", json=booking_json)
	assert add_response.status_code == status_code
	get_response = await authenticated_ac.get("/bookings/me")
	assert get_response.status_code == 200
	assert len(get_response.json()) == bookings_count

# @pytest.mark.parametrize("booking_id", [1, 2])
# async def test_booking_delete(db, authenticated_ac, booking_id):
# 	response = await authenticated_ac.delete(f"/bookings/me/delete/{booking_id}")
# 	assert response.status_code == 200
