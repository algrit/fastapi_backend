async def test_feature_add_and_get(ac):
    response_add = await ac.post("/features",
                       json={"title": "Satellite Internet"})
    assert response_add.json()["status"] == "OK"
    assert response_add.json()["data"]["title"] == "Satellite Internet"

    response_get = await ac.get("/features")
    assert response_get.json() == [response_add.json()["data"]]


