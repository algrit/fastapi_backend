async def test_hotels_get_by_date(ac):
    response = await ac.get("/hotels",
                 params={
                     "date_from": "2024-12-31",
                     "date_to": "2025-01-05"
                 })
    assert response.status_code == 200
    print(f"{response.json()=}")
