import json

import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport

from src.api.dependencies import get_db
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models import *
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
async def check_mode():
    assert settings.MODE == "TEST"


async def get_null_pool_session():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


app.dependency_overrides[get_db] = get_null_pool_session


@pytest.fixture(scope="function", autouse=True)
async def db():
    async for db in get_null_pool_session():
        yield db


@pytest.fixture(scope="session", autouse=True)
async def setup_db(check_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def mock_hotels_and_rooms(setup_db):
    with open("tests/mock_hotels.json", encoding="utf-8") as file_hotels:
        hotels_json = json.load(file_hotels)
    with open("tests/mock_rooms.json", encoding="utf-8") as file_rooms:
        rooms_json = json.load(file_rooms)

    hotels_list = [HotelAdd.model_validate(h) for h in hotels_json]
    rooms_list = [RoomAdd.model_validate(r) for r in rooms_json]

    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels_list)
        await db_.rooms.add_bulk(rooms_list)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_db, ac):
    await ac.post(
        "/auth/register",
        json={
            "email": "OmTheCat@CAT.cat",
            "password": "qwerty"
        })
