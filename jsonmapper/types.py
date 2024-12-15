from typing import Any, Callable, Self
from datetime import date, datetime
from uuid import UUID


class BaseField:

    def __init__(
            self,
            value: Any = None,
            unique: bool = False,
            nullable: bool = True,
            choices: list[Any] = None,
            default: Any = None,
            foreign_key: dict = None
    ) -> None:
        self._value = value
        self.unique = unique
        self.nullable = nullable
        self.choices = choices
        self.default = default
        self.foreign_key = foreign_key

    def _model_name(self) -> str:
        return self.__class__.__name__

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value: Any) -> None:
        self._value = value

    def _validate_wrapper(self, wrapper: Self) -> None:
        if not isinstance(wrapper, self.__class__):
            raise TypeError(f"Operand must be an instance of {self.__class__.__name__}.")

        if wrapper.value is None:
            raise ValueError("None values are not allowed")

    def _validate_value(self, value: Any) -> None:
        pass

    def _schema(self) -> dict:
        return {
            "unique": self.unique,
            "nullable": self.nullable,
            "choices": self.choices,
            "default": (
                str(type(self.default))
                if callable(self.default)
                else str(self.default)
                if isinstance(self.default, object)
                else self.default
            ),
            "foreign_key": self.foreign_key
        }

    def __str__(self):
        return (f"{self._model_name()} -> "
                f"{self._schema()}")

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


class StringField(BaseField):

    def __init__(
            self,
            value: str = None,
            max_length: int = 100,
            min_length: int = 50,
            unique: bool = False,
            nullable: bool = True,
            choices: list[Any] = None,
            default: Any = None,
            foreign_key: dict = None
    ) -> None:

        super().__init__(
            value,
            unique,
            nullable,
            choices,
            default,
            foreign_key
        )
        self.max_length = max_length
        self.min_length = min_length
        self._validate_value(value)

    def _validate_value(self, value: str) -> None:
        if value is None:
            return

        if not isinstance(value, str):
            raise TypeError("Value must be an string.")

        if (len(value) > self.max_length or
                len(value) < self.min_length):

            raise ValueError(
                f"Out of range between "
                f"<{self.max_length} or {self.min_length}>"
            )

        self.default = value

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        self._validate_value(value)
        self._value = value

    def _schema(self) -> dict:
        return {
            "max_length": self.max_length,
            "min_length": self.min_length,
            **super()._schema()
        }

    def __add__(self, other: Self) -> str:
        self._validate_wrapper(other)
        return self.value + other.value


class IntegerField(BaseField):

    def __init__(
            self,
            value: int = None,
            max_value: int = 1024,
            min_value: int = 512,
            unique: bool = False,
            nullable: bool = True,
            choices: list[Any] = None,
            default: Any = None,
            foreign_key: dict = None
    ) -> None:

        super().__init__(
            value,
            unique,
            nullable,
            choices,
            default,
            foreign_key
        )
        self.max_value = max_value
        self.min_value = min_value
        self._validate_value(value)

    def _validate_value(self, value: int) -> None:
        if value is None:
            return

        if not isinstance(value, int):
            raise TypeError("Value must be an integer.")

        if (value > self.max_value or
                value < self.min_value):

            raise ValueError(
                f"Out of range between "
                f"<{self.max_value} or {self.min_value}>"
            )

        self.default = value

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: int) -> None:
        self._validate_value(value)
        self._value = value

    def _schema(self) -> dict:
        return {
            "max_value": self.max_value,
            "min_value": self.min_value,
            **super()._schema()
        }

    def __add__(self, other: Self) -> int:
        self._validate_wrapper(other)
        return self.value + other.value

    def __sub__(self, other: Self) -> int:
        self._validate_wrapper(other)
        return self.value - other.value

    def __truediv__(self, other: Self) -> float:
        self._validate_wrapper(other)

        if other.value == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")
        return self.value / other.value

    def __floordiv__(self, other: Self) -> int:
        self._validate_wrapper(other)

        if other.value == 0:
            raise ZeroDivisionError("Floor division by zero is not allowed.")
        return self.value // other.value

    def __mul__(self, other: Self) -> int:
        self._validate_wrapper(other)
        return self.value * other.value

    def __int__(self) -> int:
        return self.value


class DateField(BaseField):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @property
    def value(self) -> date:
        return self.value

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


class FloatField(BaseField):
    ...


class ArrayField(BaseField):
    ...


class ObjectField(BaseField):
    ...


class IncrementalField(BaseField):
    ...


a = IntegerField(50, max_value=50, min_value=0)
b = IntegerField(1024, min_value=0)

c = StringField("USERS", min_length=5, max_length=5)
d = StringField("ADMIN", min_length=5)

print(a)
print(b)
