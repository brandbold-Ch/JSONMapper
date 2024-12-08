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
        self.max_length = max_length
        self.min_length = min_length
        self.unique = unique
        self.nullable = nullable
        self.choices = choices
        self.default = default
        self.foreign_key = foreign_key
        self._original_value: Any = None

    @property
    def original_value(self) -> Any:
        return self._original_value

    @original_value.setter
    def original_value(self, value: str) -> None:
        self._original_value = value

    def schema(self) -> dict:
        return {
            "max_length": self.max_length,
            "min_length": self.min_length,
            "unique": self.unique,
            "nullable": self.nullable,
            "choices": self.choices,
            "default": self.default,
            "foreign_key": self.foreign_key
        }


class StringField(BaseField):

    @property
    def original_value(self) -> str:
        return self._original_value

    @original_value.setter
    def original_value(self, value: str) -> None:
        if self.min_length <= len(value) <= self.max_length:
            self._original_value = value
        else:
            raise ValueError("Out of range")


class IntegerField(BaseField):
    ...


class DateField(BaseField):

    @property
    def original_value(self) -> date:
        return self._original_value

    @original_value.setter
    def original_value(self, value: str | date) -> None:
        if self.default is not None:
            self._original_value = value
        else:
            self._original_value = datetime.strptime(value, "%Y-%m-%d").date()


class DateTimeField(BaseField):
    ...


class BooleanField(BaseField):
    ...


class UUIDField(BaseField):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    @property
    def original_value(self) -> UUID:
        return self._original_value

    @original_value.setter
    def original_value(self, value: Callable | str) -> None:
        if isinstance(value, UUID):
            self._original_value = value
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
