from typing import Annotated

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

pk_int = Annotated[int, mapped_column(primary_key=True)]

class FeaturesORM(Base):
    __tablename__ = "features"

    id: Mapped[pk_int]
    title: Mapped[str] = mapped_column(String(100))

    rooms: Mapped[list["RoomsORM"]] = relationship(
        back_populates="features",
        secondary="rooms_features"
    )

class RoomsFeaturesORM(Base):
    __tablename__ = "rooms_features"

    id: Mapped[pk_int]
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    feature_id: Mapped[int] = mapped_column(ForeignKey("features.id"))
