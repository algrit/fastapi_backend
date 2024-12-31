from src.models.features import FeaturesORM
from src.repositories.base import BaseRepository
from src.schemas.features import Features


class FeaturesRepository(BaseRepository):
    model = FeaturesORM
    schema = Features