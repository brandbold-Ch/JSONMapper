import json
import os.path

from jsonmapper.serializer.register import Register


class SerializerJSON:

    def __init__(self) -> None:
        db_details: dict = Register.memory["db_details"]
        models_create: dict = Register.memory["models_create"]

        if os.path.exists(db_details["db_path"]):
            return

        with open(db_details["db_path"], "r") as read_json:
            json_data: dict = json.load(read_json)
            json_data["models"] = models_create

        with open(db_details["db_path"], "w") as write_json:
            json.dump(json_data, write_json, indent=2)
