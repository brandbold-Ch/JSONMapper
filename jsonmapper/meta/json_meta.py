from typing import Type, Dict, Any
from jsonmapper.serializer.register import Register
from jsonmapper.types import Field


class InspectMeta(type):

    def __new__(
            cls: Type["InspectMeta"],
            name: str,
            bases: tuple,
            dct: Dict[str, Any]
    ) -> "InspectMeta":
        if name == "Model":
            return super().__new__(cls, name, bases, dct)

        models_context = Register.data["models_create"]
        schema_fields = cls._extract_schema_fields(dct)

        models_context[name] = {
            "schema": schema_fields,
            "data": []
        }

        return super().__new__(cls, name, bases, dct)

    @staticmethod
    def _extract_schema_fields(attributes: Dict[str, Any]) -> Dict[str, Any]:
        return {
            field_name: field_value.schema_repr()
            for field_name, field_value in attributes.items()
            if isinstance(field_value, Field)
        }
