from typing import Self
from jsonmapper.types import BaseField


class JsonInspectMeta(type):
    _attrs: dict = None

    def __new__(cls, name: str, bases: tuple, fields: dict) -> Self:
        cls._attrs = fields
        return super().__new__(cls, name, bases, fields)

    def __call__(self, *args, **kwargs) -> Self:
        attr_count = 0

        for field, value in self._attrs.items():
            if not isinstance(value, BaseField):
                continue

            field_value = (
                value.default() if callable(value.default) else value.default
                if value.default is not None
                else args[attr_count]
            )

            setattr(self, field, field_value)
            value.value = field_value

            if value.default is None:
                attr_count += 1

        return self
