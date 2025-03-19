import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.database import Base

if typing.TYPE_CHECKING:
	from src.models.features import FeaturesORM


class RoomsORM(Base):
	__tablename__ = "rooms"

	id: Mapped[int] = mapped_column(primary_key=True)
	hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
	title: Mapped[str]
	description: Mapped[str | None]
	price: Mapped[int]
	quantity: Mapped[int]

	features: Mapped[list["FeaturesORM"]] = relationship(
		back_populates="rooms",
		secondary="rooms_features"
	)
