import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.config import settings

async_engine = create_async_engine(url=settings.DB_URL)

async_session_maker = async_sessionmaker(bind=async_engine, expire_on_commit=False)

class Base(DeclarativeBase):
	pass