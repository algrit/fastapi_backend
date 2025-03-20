from datetime import date

from src.api.dependencies import PaginationDep
from src.schemas.hotels import HotelAdd, HotelPatch
from src.services.base import BaseService
from src.services.utils import DateChecker


class HotelService(BaseService, DateChecker):
    async def get_free_hotels_by_date_service(
        self,
        pagination: PaginationDep,
        date_from: date,
        date_to: date,
        title: str | None = None,
        location: str | None = None,
    ):
        per_page = pagination.per_page or 5
        self.date_check(date_from=date_from, date_to=date_to)
        return await self.db.hotels.get_hotels_by_date(
            date_from=date_from,
            date_to=date_to,
            title=title,
            location=location,
            limit=per_page,
            offset=(pagination.page - 1) * per_page,
        )

    async def hotel_get_by_id_service(self, hotel_id: int):
        hotel = await self.db.hotels.get_one(id=hotel_id)
        return hotel

    async def hotel_add_service(self, hotel_data: HotelAdd):
        added_hotel = await self.db.hotels.add_one(hotel_data)
        await self.db.commit()
        return added_hotel

    async def hotel_put_service(self, hotel_id: int, hotel: HotelAdd):
        await self.db.hotels.edit(hotel, id=hotel_id)
        await self.db.commit()

    async def hotel_patch_service(self, hotel_id: int, hotel: HotelPatch):
        await self.db.hotels.edit(hotel, exclude_unset=True, id=hotel_id)
        await self.db.commit()

    async def hotel_delete_service(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()
