from typing import Self, Any
from jsonmapper.serializer.register import Register
from jsonmapper.types import BaseField
from jsonmapper.serializer.creator import SerializerJSON


class JsonInspectMeta(type):

    def __new__(cls, name: str, bases: tuple, dct: dict) -> Self:
        ctx: dict = Register.memory["models_create"]
        type_schema: dict = {}

        for field, value in dct.items():
            if isinstance(value, BaseField) is False:
                continue
            type_schema.update({field: value.schema()})

        if name not in ["Model", "JsonStore"]:
            ctx.update({
                name: {
                    "schema": type_schema,
                    "data": []
                }
            })

        return super().__new__(cls, name, bases, dct)

    def __call__(self, *args, **kwargs) -> Any:
        if self.__name__ != "JsonStore":
            SerializerJSON()
        return super().__call__(*args, **kwargs)
