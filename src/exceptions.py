class AppException(Exception):
	detail = "unexpected error"

	def __init__(self, *args, **kwargs):
		super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(AppException):
	detail = "Object not found"


class NoFreeRoomsException(AppException):
	detail = "Can't book this room. No free rooms for these dates"
