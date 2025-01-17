from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.features import FeatureAdd
from src.tasks.tasks import test_task

router = APIRouter(prefix="/features", tags=["Удобства номера"])


@router.get("", summary="Получить все удобства")
@cache(expire=10)
async def features_get(db: DBDep):
    return await db.features.get_all()


@router.post("", summary="Добавление удобства в список возможных удобств")
async def feature_add(db: DBDep, feature: FeatureAdd):
    added_feature = await db.features.add_one(feature)
    await db.commit()

    test_task.delay()

    return {"status": "OK", "data": added_feature}
