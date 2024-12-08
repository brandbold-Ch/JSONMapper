
class SerializerJSON:

    def __init__(self, *args, **kwargs) -> None:
        self.json_base: dict = {}

    def create_schema(self) -> None:
        ...

    def create_model(self) -> None:
        ...
