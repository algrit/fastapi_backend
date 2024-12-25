from sqlalchemy import select, insert

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.schemas.rooms import Room, RoomAdd


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_all(self,
                      hotel_id,
                      title,
                      description,
                      price,
                      quantity,
                      ):
        query = select(RoomsOrm)
        if hotel_id:
            query = query.filter_by(hotel_id=hotel_id)
        if title:
            query = query.filter(RoomsOrm.title.contains(title))
        if description:
            query = query.filter(RoomsOrm.description.contains(description))
        if price:
            query = query.filter(RoomsOrm.price.__le__(price))
        rooms = await self.session.execute(query)
        return [Room.model_validate(room, from_attributes=True) for room in rooms.scalars().all()]

    async def add_one(self, hotel_id: int, title: str, price, quantity):
        add_room_stmt = insert(RoomsOrm).values(hotel_id=hotel_id, title=title, price=price,
                                                quantity=quantity).returning(self.model)
        result = await self.session.execute(add_room_stmt)
        room = result.scalars().one()
        return Room.model_validate(room, from_attributes=True)
