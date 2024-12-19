import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text

from src.config import settings

async_engine = create_async_engine(url=settings.DB_URL)

async_session_maker = async_sessionmaker(bind=async_engine, expire_on_commit=False)

async def func():
	async with async_session_maker() as conn:
		query = text("SELECT version()")
		res = await conn.execute(query)
		print(res.fetchone())

asyncio.run(func())