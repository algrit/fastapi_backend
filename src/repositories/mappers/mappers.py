from src.repositories.mappers.base import DataMapper
from src.models.users import UsersORM
from src.models.bookings import BookingsORM
from src.models.features import FeaturesORM
from src.models.hotels import HotelsORM
from src.models.rooms import RoomsOrm
from src.schemas.users import User, UserWithHashedPass
from src.schemas.bookings import Booking
from src.schemas.features import Feature
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room, RoomWithRels


class UserDataMapper(DataMapper):
    db_model = UsersORM
    schema = User


class UserWithHashedPassDataMapper(DataMapper):
    db_model = UsersORM
    schema = UserWithHashedPass


class HotelDataMapper(DataMapper):
    db_model = HotelsORM
    schema = Hotel


class RoomDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Room


class RoomWithRelsDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = RoomWithRels


class FeatureDataMapper(DataMapper):
    db_model = FeaturesORM
    schema = Feature


class BookingDataMapper(DataMapper):
    db_model = BookingsORM
    schema = Booking
