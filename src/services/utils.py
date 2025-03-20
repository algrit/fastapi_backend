from datetime import date

from src.exceptions import WrongDatesException


class DateChecker:
    @staticmethod
    def date_check(date_from: date, date_to: date):
        if date_from >= date_to:
            raise WrongDatesException

