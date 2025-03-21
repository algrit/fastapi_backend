import pytest


@pytest.mark.parametrize("hotel_id, title, description, price, quantity, features_ids")
async def test_rooms_crud(ac, hotel_id: int, title: str, description: str, price: int, quantity: int,
                          features_ids: list[int]):
    pass
