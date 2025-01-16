from fastapi import APIRouter
import json

from src.init import redis_manager

from src.api.dependencies import DBDep
from src.schemas.features import FeatureAdd

router = APIRouter(prefix="/features", tags=["Удобства номера"])


@router.get("", summary="Получить все удобства")
async def features_get(db: DBDep):
    features_from_cache = await redis_manager.get("features")
    if not features_from_cache :
        # print("ебашу в базу")
        features = await db.features.get_all()
        await redis_manager.set("features", json.dumps([f.model_dump() for f in features]), expire=1)
        return features
    else:
        # print("ЕБАШУ В КЭШ")
        features = json.loads(features_from_cache)
        return features


@router.post("", summary="Добавление удобства в список возможных удобств")
async def feature_add(db: DBDep, feature: FeatureAdd):
    added_feature = await db.features.add_one(feature)
    await db.commit()
    return {"status": "OK", "data": added_feature}
