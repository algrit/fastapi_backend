from sqlalchemy import select, insert, delete

from src.models.features import FeaturesORM, RoomsFeaturesORM
from src.repositories.base import BaseRepository
from src.schemas.features import Feature, RoomFeature


class FeaturesRepository(BaseRepository):
    model = FeaturesORM
    schema = Feature


class RoomsFeaturesRepository(BaseRepository):
    model = RoomsFeaturesORM
    schema = RoomFeature

    async def update_rooms_features(self, room_id: int, new_features: list[int]):
        query = select(RoomsFeaturesORM.feature_id).filter_by(room_id=room_id)
        result = await self.session.execute(query)
        features_ids = result.scalars().all()
        features_to_delete = set(features_ids) - set(new_features)
        features_to_add = set(new_features) - set(features_ids)
        if features_to_delete:
            features_m2m_delete_stmt = (
                delete(RoomsFeaturesORM)
                .filter(RoomsFeaturesORM.room_id == room_id,
                        RoomsFeaturesORM.feature_id.in_(features_to_delete)))
            await self.session.execute(features_m2m_delete_stmt)
        if features_to_add:
            features_m2m_add_stmt = (
                insert(RoomsFeaturesORM)
                .values(*[{"room_id": room_id, "feature_id": f_id} for f_id in features_to_add])
            )
            await self.session.execute(features_m2m_add_stmt)
