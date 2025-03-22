class AppException(Exception):
    detail = "unexpected error"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(AppException):
    detail = "Объект не найден"


class UniquenessViolationException(AppException):
    detail = "Нарушение уникальности поля"


class ForeignKeyViolationException(AppException):
    detail = "Нарушение внешнего ключа"


class WrongDatesException(AppException):
    detail = "Дата выезда должна быть позже даты заезда"


class NoFreeRoomsException(AppException):
    detail = "Невозможно забронировать. Номер занят на указанные даты"


class WrongPassword(AppException):
    detail = "Неверный пароль"


class WrongAccessKey(AppException):
    detail = "Неверный ключ доступа"
