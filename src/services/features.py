from src.schemas.features import FeatureAdd
from src.services.base import BaseService


class FeatureService(BaseService):
    async def features_get_service(self):
        return await self.db.features.get_all()

    async def feature_add_service(self, feature: FeatureAdd):
        added_feature = await self.db.features.add_one(feature)
        await self.db.commit()
        return added_feature
