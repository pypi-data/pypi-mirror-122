from datetime import date, datetime
from typing import Union

from openpyxl.utils.datetime import from_excel, to_excel


def ensure_python_date(value: Union[float, int, date, datetime]) -> date:
    """
    Interpret the value, which may be a Python date or datetime, or an Excel serial date,
    and return a Python date object.
    >>> ensure_python_date(10)
    datetime.date(1900, 1, 10)
    >>> ensure_python_date(10.5)
    datetime.date(1900, 1, 10)
    >>> ensure_python_date(datetime(2020, 1, 2, 3, 4, 5))
    datetime.date(2020, 1, 2)
    >>> ensure_python_date(date(2020, 1, 2))
    datetime.date(2020, 1, 2)
    """
    if isinstance(value, (float, int)):
        # The given value is an Excel date or datetime serial number.
        # Convert it, and throw away the time part.
        return from_excel(value).date()

    if isinstance(value, datetime):
        # The given value is a datetime object.
        # Just throw away the time part.
        return value.date()

    if isinstance(value, date):
        # The given value is already the desired type.
        return value

    raise TypeError("Failed to convert value to date.")


def ensure_python_datetime(value: Union[float, int, date, datetime]) -> datetime:
    """
    Interpret the value, which may be a Python date or datetime, or an Excel serial date,
    and return a Python datetime object.
    >>> ensure_python_datetime(10)
    datetime.datetime(1900, 1, 10, 0, 0)
    >>> ensure_python_datetime(10.5)
    datetime.datetime(1900, 1, 10, 12, 0)
    >>> ensure_python_datetime(datetime(2020, 1, 2, 3, 4, 5))
    datetime.datetime(2020, 1, 2, 3, 4, 5)
    >>> ensure_python_datetime(date(2020, 1, 2))
    datetime.datetime(2020, 1, 2, 0, 0)
    """
    if isinstance(value, (float, int)):
        # The given value is an Excel date or datetime serial number.
        # Convert it.
        return from_excel(value)

    if isinstance(value, datetime):
        # The given value is already the desired type.
        return value

    if isinstance(value, date):
        # The given value is a date without time. Assume midnight of that day.
        return datetime.combine(value, datetime.min.time())

    raise TypeError("Failed to convert value to datetime.")


def ensure_excel_date(value: Union[float, int, date, datetime]) -> int:
    """
    Interpret the value, which may be a Python date or datetime, or an Excel serial date,
    and return an integer, representing an Excel serial date.
    >>> ensure_excel_date(10)
    10
    >>> ensure_excel_date(10.5)
    10
    >>> ensure_excel_date(datetime(2020, 1, 2, 3, 4, 5))
    43832
    >>> ensure_excel_date(date(2020, 1, 2))
    43832
    """
    if isinstance(value, (float, int)):
        # The given value is already an Excel date or datetime serial number.
        # Casting to int throws away the time and keeps the date.
        return int(value)

    if isinstance(value, datetime):
        # The given value is a datetime object.
        # Throw away the time part and convert to Excel format.
        return int(to_excel(value.date()))

    if isinstance(value, date):
        # The given value is a date object.
        # Convert to Excel format.
        return int(to_excel(value))


def ensure_excel_datetime(value: Union[float, int, date, datetime]) -> float:
    """
    Interpret the value, which may be a Python date or datetime, or an Excel serial date,
    and return a float, representing an Excel serial datetime.
    >>> ensure_excel_datetime(10)
    10.0
    >>> ensure_excel_datetime(10.5)
    10.5
    >>> ensure_excel_datetime(datetime(2020, 1, 2, 3, 4, 5))
    43832.12783564815
    >>> ensure_excel_datetime(date(2020, 1, 2))
    43832.0
    """
    if isinstance(value, (float, int)):
        # The given value is already an Excel date or datetime serial number.
        return float(value)

    if isinstance(value, (datetime, date)):
        # The given value is a datetime object.
        # Convert to Excel format.
        return float(to_excel(value))
