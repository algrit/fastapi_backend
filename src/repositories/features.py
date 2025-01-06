from src.models.features import FeaturesORM, RoomsFeaturesORM
from src.repositories.base import BaseRepository
from src.schemas.features import Feature, RoomFeature


class FeaturesRepository(BaseRepository):
    model = FeaturesORM
    schema = Feature


class RoomsFeaturesRepository(BaseRepository):
    model = RoomsFeaturesORM
    schema = RoomFeature