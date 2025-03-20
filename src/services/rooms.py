from datetime import date

from src.exceptions import ObjectNotFoundException
from src.schemas.features import RoomFeatureAdd
from src.schemas.rooms import RoomAddRequest, RoomAdd, RoomPatchRequest, RoomPatch
from src.services.base import BaseService
from src.services.utils import DateChecker, HotelExistenceChecker


class RoomService(BaseService, DateChecker, HotelExistenceChecker):
    async def get_free_rooms_by_date_service(self, hotel_id: int, date_from: date, date_to: date):
        self.date_check(date_from=date_from, date_to=date_to)
        await self.hotel_existence_check(self.db, hotel_id)
        free_rooms = await self.db.rooms.get_rooms_by_date(hotel_id, date_from, date_to)
        return free_rooms

    async def room_get_by_id_service(self, hotel_id: int, room_id: int):
        room = await self.db.rooms.get_one(hotel_id=hotel_id, id=room_id)
        if not room:
            raise ObjectNotFoundException
        return room

    async def room_add_service(self, hotel_id: int, data: RoomAddRequest):
        await self.hotel_existence_check(self.db, hotel_id)
        data_with_hotel = RoomAdd(hotel_id=hotel_id, **data.model_dump())
        added_room = await self.db.rooms.add_one(data_with_hotel)
        if data.features_ids:
            features_list = [
                RoomFeatureAdd(room_id=added_room.id, feature_id=f_id) for f_id in data.features_ids
            ]
            await self.db.room_features.add_bulk(features_list)
        await self.db.commit()
        return added_room

    async def room_put_service(self, hotel_id: int, room_id: int, data: RoomAddRequest):
        await self.hotel_existence_check(self.db, hotel_id)
        _room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
        await self.db.rooms.edit(_room_data, id=room_id)
        await self.db.room_features.update_rooms_features(room_id, data.features_ids)
        await self.db.commit()

    async def room_patch_service(self, hotel_id: int, room_id: int, data: RoomPatchRequest):
        await self.hotel_existence_check(self.db, hotel_id)
        if any([data.title, data.description, data.price, data.quantity]):
            _room_data = RoomPatch(hotel_id=hotel_id, **data.model_dump(exclude_unset=True))
            await self.db.rooms.edit(_room_data, exclude_unset=True, id=room_id)
        if getattr(data, "features_ids", None):
            await self.db.room_features.update_rooms_features(room_id, data.features_ids)
        await self.db.commit()

    async def room_delete_service(self, hotel_id: int, room_id: int):
        await self.hotel_existence_check(self.db, hotel_id)
        filter_by = {"hotel_id": hotel_id, "id": room_id}
        await self.db.rooms.delete(**filter_by)
        await self.db.commit()
