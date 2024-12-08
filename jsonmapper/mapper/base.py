from typing import Self
import os
import json
from jsonmapper.meta.json_meta import JsonInspectMeta
from jsonmapper.types import BaseField
from jsonmapper.serializer.register import Register


class Model(metaclass=JsonInspectMeta):

    def __new__(cls, *args, **kwargs) -> Self:
        if len(args) > 0:
            raise ValueError("No arguments allowed")

        for field, value in cls.__dict__.items():
            if not isinstance(value, BaseField):
                continue

            if value.default is not None:
                setter_value = (
                    value.default() if callable(value.default)
                    else value.default
                )
                setattr(cls, field, setter_value)
                continue

            value.original_value = kwargs.get(field)
            setattr(cls, field, value.original_value)

        return super().__new__(cls)


class JsonStore(metaclass=JsonInspectMeta):

    def __init__(self, db_path: str, db_name: str = "database") -> None:
        ctx: dict = Register.memory["db_details"]

        if os.path.exists(db_path):
            with open(f"{db_name}.json", "w") as data:
                json.dump({}, data, indent=4)

            ctx["db_path"] = db_path
            ctx["db_name"] = db_name
        else:
            raise FileNotFoundError("Route not found")
