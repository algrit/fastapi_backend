import pytest
from httpx import AsyncClient, ASGITransport

from src.config import settings
from src.database import Base, engine_null_pool
from src.main import app
from src.models import *


@pytest.fixture(scope="session", autouse=True)
async def check_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_db(check_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


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
