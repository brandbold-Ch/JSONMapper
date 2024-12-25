from collections.abc import Callable
from datetime import date


def is_number(func: Callable):
    def wrapper(*args, **kwargs):
        if not isinstance(args[1], int):
            raise TypeError("Value must be an integer.")
        return func(*args, **kwargs)
    return wrapper


def is_string(func: Callable):
    def wrapper(*args, **kwargs):
        if not isinstance(args[1], str):
            raise TypeError("Value must be an string.")
        return func(*args, **kwargs)
    return wrapper


def is_boolean(func: Callable):
    def wrapper(*args, **kwargs):
        if not isinstance(args[1], bool):
            raise TypeError("Value must be an boolean.")
        return func(*args, **kwargs)
    return wrapper


def is_date(func: Callable):
    def wrapper(*args, **kwargs):
        if not isinstance(args[1], date):
            raise TypeError("Value must be an date.")
        return func(*args, **kwargs)
    return wrapper


def is_string_or_date(func: Callable):
    def wrapper(*args, **kwargs):
        if (not isinstance(args[1], str)
                and not isinstance(args[1], date)):
            raise TypeError("Value must be an string or date.")
        return func(*args, **kwargs)
    return wrapper

