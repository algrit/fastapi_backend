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
    detail = "Can't book this room. No free rooms for these dates"
