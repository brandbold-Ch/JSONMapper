from typing import Any, Callable
from datetime import date, datetime
from uuid import UUID


class BaseField:

    def __init__(
        self,
        max_length: int = 255,
        min_length: int = 0,
        unique: bool = False,
        nullable: bool = True,
        choices: list[Any] = None,
        default: Any = None,
        foreign_key: dict[str, str] = None
    ) -> None:
        self.max_length = max_length,
        self.min_length = min_length,
        self.unique = unique,
        self.nullable = nullable,
        self.choices = choices,
        self.default = default
        self.foreign_key = foreign_key
        self._value: Any = None

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        self._value = value


class StringField(BaseField):

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        if self.min_length[0] <= len(value) <= self.max_length[0]:
            self._value = value
        else:
            raise ValueError("Out of range")


class IntegerField(BaseField):
    ...


class DateField(BaseField):

    @property
    def value(self) -> date:
        return self._value

    @value.setter
    def value(self, value: str | date) -> None:
        if self.default is not None:
            self._value = value
        else:
            self._value = datetime.strptime(value, "%Y-%m-%d").date()


class DateTimeField(BaseField):
    ...


class BooleanField(BaseField):
    ...


class UUIDField(BaseField):

    def __init__(
        self,
        max_length: int = 255,
        min_length: int = 0,
        unique: bool = False,
        nullable: bool = True,
        choices: list[Any] = None,
        default: Any = None,
        foreign_key: dict[str, str] = None
    ) -> None:
        super().__init__(
            max_length,
            min_length,
            unique,
            nullable,
            choices,
            default,
            foreign_key
        )
        self.max_length = max_length,
        self.min_length = min_length,
        self.unique = unique,
        self.nullable = nullable,
        self.choices = choices,
        self.default = default
        self.foreign_key = foreign_key
        self._value: Any = None

    @property
    def value(self) -> UUID:
        return self._value

    @value.setter
    def value(self, value: Callable) -> None:
        if isinstance(value, UUID):
            self._value = value
        else:
            raise TypeError("It is not of type UUID")


class FloatField(BaseField):
    ...


class ArrayField(BaseField):
    ...


class ObjectField(BaseField):
    ...


class IncrementalField(BaseField):
    ...
