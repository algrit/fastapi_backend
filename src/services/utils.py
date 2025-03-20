from datetime import date

from src.exceptions import WrongDatesException, ObjectNotFoundException
from src.utils.db_manager import DBManager


class DateChecker:
    @staticmethod
    def date_check(date_from: date, date_to: date):
        if date_from >= date_to:
            raise WrongDatesException


class HotelExistenceChecker:
    @staticmethod
    async def hotel_existence_check(db: DBManager, hotel_id: int):
        hotel = await db.hotels.get_one(id=hotel_id)
        if not hotel:
            raise ObjectNotFoundException
