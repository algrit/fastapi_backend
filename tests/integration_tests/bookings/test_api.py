async def test_booking_add(db, authenticated_ac):
    room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post("/bookings",
                                     json={
                                         "room_id": room_id,
                                         "date_from": "2024-02-01",
                                         "date_to": "2024-02-03",
                                     })
    assert response.json()["status"] == "OK"
    assert "data" in response.json()
