import pytest


@pytest.mark.parametrize("title", ["Satellite Internet", "towels", "shampoo"])
async def test_feature_add_and_get(ac, title):
    response_add = await ac.post("/features", json={"title": title})
    assert response_add.json()["status"] == "OK"
    assert response_add.json()["data"]["title"] == title

    response_get = await ac.get("/features")
    assert response_get.json() is not None
