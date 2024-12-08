import json
from jsonmapper.serializer.register import Register


class SerializerJSON:

    def __init__(self) -> None:
        db_details: dict = Register.memory["db_details"]
        models_create: dict = Register.memory["models_create"]

        with open(f"{db_details['db_name']}.json", "w") as data:
            json.dump(models_create, data, indent=2)
