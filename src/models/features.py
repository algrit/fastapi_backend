from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class FeaturesORM(Base):
    __tablename__ = "features"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))


class FeaturesRoomsORM(Base):
    __tablename__ = "rooms_features"

    id: Mapped[int] = mapped_column(primary_key=True)
    feature_id: Mapped[int] = mapped_column(ForeignKey("features.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
