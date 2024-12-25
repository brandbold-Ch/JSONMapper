import json
from jsonmapper.serializer.register import Register


class SerializerJSON:

    def __init__(self) -> None:
        db_details: dict = Register.data["db_details"]
        models_create: dict = Register.data["models_create"]

        with open(db_details["db_path"], "r") as read_json:
            json_data: dict = json.load(read_json)
            json_data["models"] = models_create

        with open(db_details["db_path"], "w") as write_json:
            json.dump(json_data, write_json, indent=2)
