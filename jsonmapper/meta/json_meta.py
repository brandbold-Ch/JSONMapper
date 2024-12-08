from typing import Self, Any


class JsonInspectMeta(type):

    def __new__(cls, name: str, bases: tuple, dct: dict) -> Self:
        return super().__new__(cls, name, bases, dct)

    def __call__(self, *args, **kwargs) -> Any:
        subclass = super().__call__(*args, **kwargs)
        print(kwargs)
        return subclass
