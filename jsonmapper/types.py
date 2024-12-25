from typing import Any, Callable, Self, List, Optional, Union
from datetime import date, datetime
from uuid import UUID
from jsonmapper.decorators.types import is_number, is_string, is_date, is_string_or_date
from abc import ABC, abstractmethod


class Field(ABC):
    def __init__(
        self,
        value: Any = None,
        unique: bool = False,
        nullable: bool = True,
        choices: List[Any] = None,
        default: Any = None,
        foreign_key: dict = None,
        primary_key: bool = False,
        is_odm_field: bool = True
    ) -> None:

        self._value = value
        self.unique = unique
        self.nullable = nullable
        self.choices = choices
        self.default = default
        self.foreign_key = foreign_key
        self.primary_key = primary_key
        self.is_odm_field = is_odm_field

    def wrapper(self) -> str:
        return self.__class__.__name__

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value: Any) -> None:
        self._value = value

    def unwrap(self) -> Any:
        return self._value

    def _validate_wrapper(self, wrapper: Self) -> None:
        if not isinstance(wrapper, self.__class__):
            raise TypeError(f"Operand must be an instance of {self.wrapper()}.")

        if wrapper.value is None:
            raise ValueError("None values are not allowed.")

    def _validate_constraints(self) -> None:
        if self.primary_key:
            self.nullable = False
            self.unique = True

        if self._value is None and not self.nullable:
            raise ValueError("None values are not allowed.")

        if self.default is not None:
            if callable(self.default):
                self._value = self.default()
            else:
                self._value = self.default

    def __str__(self) -> str:
        return f"{self.wrapper()}({self._value})"

    def schema_repr(self) -> dict:
        return {
            "unique": self.unique,
            "nullable": self.nullable,
            "choices": self.choices,
            "foreign_key": self.foreign_key,
            "default": (
                str(type(self.default))
                if callable(self.default)
                else str(self.default)
                if isinstance(self.default, object)
                else self.default
            )
        }

    def __int__(self) -> None:
        raise TypeError("Unsupported cast <int>")

    def __float__(self) -> None:
        raise TypeError("Unsupported cast <float>")

    def __bool__(self) -> None:
        raise TypeError("Unsupported cast <bool>")

    def __add__(self, other) -> None:
        raise TypeError("Unsupported operation < + >")

    def __sub__(self, other) -> None:
        raise TypeError("Unsupported operation < - >")

    def __truediv__(self, other) -> None:
        raise TypeError("Unsupported operation < / >")

    def __floordiv__(self, other) -> None:
        raise TypeError("Unsupported operation < // >")


class StringField(Field):
    def __init__(
        self,
        value: str = None,
        max_length: int = 100,
        min_length: int = 50,
        unique: bool = False,
        nullable: bool = True,
        choices: List[Any] = None,
        default: Any = None,
        foreign_key: dict = None,
        primary_key: bool = False,
        is_odm_field: bool = True
    ) -> None:

        super().__init__(
            value,
            unique,
            nullable,
            choices,
            default,
            foreign_key,
            primary_key,
            is_odm_field
        )
        self.max_length = max_length
        self.min_length = min_length

    def _validate_constraints(self) -> None:
        super()._validate_constraints()

        if (len(self.value) > self.max_length or
                len(self.value) < self.min_length):
            raise ValueError(
                f"Out of range between "
                f"<{self.max_length} or {self.min_length}>"
            )

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    @is_string
    def value(self, value: str) -> None:
        self._value = value

        if self.is_odm_field:
            self._validate_constraints()

    def unwrap(self) -> str:
        return self._value

    def schema_repr(self) -> dict:
        return {
            "max_length": self.max_length,
            "min_length": self.min_length,
            **super().schema_repr()
        }

    def __add__(self, other: Self) -> str:
        self._validate_wrapper(other)
        return self._value + other.value


class IntegerField(Field):
    def __init__(
        self,
        value: int = None,
        max_value: int = 1024,
        min_value: int = 0,
        unique: bool = False,
        nullable: bool = True,
        choices: List[Any] = None,
        default: Any = None,
        foreign_key: dict = None,
        primary_key: bool = False,
        is_odm_field: bool = True
    ) -> None:

        super().__init__(
            value,
            unique,
            nullable,
            choices,
            default,
            foreign_key,
            primary_key,
            is_odm_field
        )
        self.max_value = max_value
        self.min_value = min_value

        if self.is_odm_field:
            self._validate_constraints()

    def _validate_constraints(self) -> None:
        super()._validate_constraints()

        if (self.value > self.max_value or
                self.value < self.min_value):
            raise ValueError(
                f"Out of range between "
                f"<{self.max_value} or {self.min_value}>"
            )

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    @is_number
    def value(self, value: int) -> None:
        self._value = value

        if self.is_odm_field:
            self._validate_constraints()

    def unwrap(self) -> int:
        return self._value

    def schema_repr(self) -> dict:
        return {
            "max_value": self.max_value,
            "min_value": self.min_value,
            **super().schema_repr()
        }

    def __add__(self, other: Self) -> int:
        self._validate_wrapper(other)
        return self._value + other.value

    def __sub__(self, other: Self) -> int:
        self._validate_wrapper(other)
        return self._value - other.value

    def __truediv__(self, other: Self) -> float:
        self._validate_wrapper(other)

        if other.value == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")
        return self._value / other.value

    def __floordiv__(self, other: Self) -> int:
        self._validate_wrapper(other)

        if other.value == 0:
            raise ZeroDivisionError("Floor division by zero is not allowed.")
        return self._value // other.value

    def __mul__(self, other: Self) -> int:
        self._validate_wrapper(other)
        return self._value * other.value

    def __int__(self) -> int:
        return self._value

    def __float__(self) -> float:
        return float(self._value)


class DateField(Field):
    def __init__(
        self,
        value: date | str = None,
        max_date: date | str = None,
        min_date: date | str = None,
        format_date: str = "%Y-%m-%d",
        unique: bool = False,
        nullable: bool = True,
        choices: List[Any] = None,
        default: Any = None,
        foreign_key: dict = None,
        primary_key: bool = False,
        is_odm_field: bool = True
    ) -> None:

        super().__init__(
            value,
            unique,
            nullable,
            choices,
            default,
            foreign_key,
            primary_key,
            is_odm_field
        )
        self.max_date = max_date
        self.min_date = min_date
        self.format_date = format_date

        if self.is_odm_field:
            self._validate_constraints()

    @is_string
    def _to_date(self, value: str) -> date:
        return datetime.strptime(value, self.format_date).date()

    def _validate_dates(
        self,
        _max: Union[str, date],
        _min: Union[str, date]
    ) -> None:
        if _max is None or _min is None:
            return

        if not isinstance(_max, date) or not isinstance(_max, str):
            raise TypeError("Max date must be a date or string.")

        if not isinstance(_min, date) or not isinstance(_min, str):
            raise TypeError("Min date must be a date or string.")

    def _validate_constraints(self) -> None:
        super()._validate_constraints()
        split_date = str(self.value).split("-")

        if len(split_date) != 3:
            raise ValueError(f"Invalid format, format must be {self.format_date}")

        if not all(map(lambda item: item.isnumeric(), split_date)):
            raise ValueError("Invalid format date, must be numeric")

    @property
    def value(self) -> date:
        return self._value

    @value.setter
    @is_string_or_date
    def value(self, value: Union[str, date]) -> None:
        self._value = (
            self._to_date(value)
            if isinstance(value, str) else value)

        if self.is_odm_field:
            self._validate_constraints()

    def schema_repr(self) -> dict:
        return {
            "max_date": self.max_date,
            "min_date": self.min_date,
            **super().schema_repr()
        }


class DateTimeField(Field):
    ...


class BooleanField(Field):
    ...


class UUIDField(Field):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    @property
    def value(self) -> UUID:
        return self.value

    @value.setter
    def value(self, value: Callable | str) -> None:
        if isinstance(value, UUID):
            self._value = value
        else:
            raise TypeError("It is not of type UUID")


class FloatField(Field):
    ...


class ArrayField(Field):
    ...


class ObjectField(Field):
    ...


class IncrementalField(Field):
    ...


example1 = IntegerField(-1, is_odm_field=False)
example2 = IntegerField(6, is_odm_field=False)
example3 = IntegerField(67, is_odm_field=True)
example3.value = 900

print(example1 + example3)
print(example1)
