from sqlalchemy import delete

from src.models.features import FeaturesORM, RoomsFeaturesORM
from src.repositories.base import BaseRepository
from src.schemas.features import Feature, RoomFeature


class FeaturesRepository(BaseRepository):
    model = FeaturesORM
    schema = Feature


class RoomsFeaturesRepository(BaseRepository):
    model = RoomsFeaturesORM
    schema = RoomFeature

    async def delete_bulk(self, room_id: int, features: list[int]) -> None:
        stmt = (
            delete(RoomsFeaturesORM)
            .filter(
                RoomsFeaturesORM.room_id == room_id,
                RoomsFeaturesORM.feature_id.in_(features)
            )
        )
        await self.session.execute(stmt)
