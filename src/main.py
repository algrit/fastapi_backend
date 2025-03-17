from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.init import redis_manager

from src.api.auth import router as auth_router
from src.api.hotels import router as hotels_router
from src.api.rooms import router as rooms_router
from src.api.bookings import router as bookings_router
from src.api.features import router as features_router
from src.api.images import router as images_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    yield
    await redis_manager.close()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(bookings_router)
app.include_router(features_router)
app.include_router(images_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=9000, reload=True)
