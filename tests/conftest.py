import json

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text

from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool, async_session_maker
from src.main import app
from src.models import *
from src.schemas.hotels import HotelAdd


@pytest.fixture(scope="session", autouse=True)
async def check_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_db(check_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def mock_hotels_and_rooms(setup_db):
    mock_hotels = open("tests/mock_hotels.json", "r")
    hotels_json = json.load(mock_hotels)
    mock_rooms = open("tests/mock_rooms.json", "r")
    rooms_json = json.load(mock_rooms)
    async with async_session_maker() as session:
        hotels_list = [HotelsORM(title=h["title"], location=h["location"]) for h in hotels_json]
        session.add_all(hotels_list)
        await session.flush()
        rooms_list = [RoomsORM(hotel_id=r["hotel_id"],
                               title=r["title"],
                               description=r["description"],
                               price=r["price"],
                               quantity=r["quantity"]) for r in rooms_json]
        session.add_all(rooms_list)
        await session.commit()


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_db):
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        await ac.post(
            "/auth/register",
            json={
                "email": "OmTheCat@CAT.cat",
                "password": "qwerty"
            })
