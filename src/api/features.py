from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.features import FeatureAdd
from src.services.features import FeatureService

router = APIRouter(prefix="/features", tags=["Удобства номера"])


@router.get("", summary="Получить все удобства")
@cache(expire=180)
async def features_get(db: DBDep):
    return await FeatureService(db).features_get_service()


@router.post("", summary="Добавление удобства в список возможных удобств")
async def feature_add(db: DBDep, feature: FeatureAdd):
    added_feature = await FeatureService(db).feature_add_service(feature)
    return {"status": "Feature added", "added feature": added_feature}
