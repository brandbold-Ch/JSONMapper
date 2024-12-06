from pickle import PROTO

from jsonmapper.meta.agents import AnnotatedMeta
from uuid import uuid4
from typing import Any


class BaseField(metaclass=AnnotatedMeta):

    def __init__(
        self,
        max_length: int = None,
        min_length: int = None,
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

    def serialize(self):
        ...

    def __setattr__(self, key, value):
        constrains = [
            "max_length",
            "min_length",
            "unique",
            "nullable",
            "choices",
            "default",
            "foreign_key"
        ]

        if key not in constrains:
            raise ValueError(f"Restriction not allowed for: {key}")

        super().__setattr__(key, value)


class String(BaseField):
    ...


class Integer(BaseField):
    ...


class Date(BaseField):
    ...


class DateTime(BaseField):
    ...


class Boolean(BaseField):
    ...


class UUID(BaseField):
    ...


class Float(BaseField):
    ...


class Array(BaseField):
    ...


class Object(BaseField):
    ...


class IncrementalId(BaseField):
    ...


a = UUID(default=uuid4())
print(a.default)
