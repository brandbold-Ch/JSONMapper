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

        if len(kwargs) > 0:
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

                value._value = kwargs.get(field)
                setattr(cls, field, value._value)

        return super().__new__(cls)


class JsonStore(metaclass=JsonInspectMeta):

    def __init__(self, db_path: str = "/", db_name: str = "database.json") -> None:
        ctx: dict = Register.memory["db_details"]
        path = f"{os.getcwd()}{db_path}"
        file_path = os.path.normpath(f"{path}/{db_name}.json")

        if os.path.exists(path):
            ctx["db_path"] = file_path
            ctx["db_name"] = db_name

            if os.path.exists(file_path):
                return

            with open(file_path, "w") as data:
                json.dump({"details": ctx}, data, indent=4)

        else:
            raise FileNotFoundError("Route not found")
