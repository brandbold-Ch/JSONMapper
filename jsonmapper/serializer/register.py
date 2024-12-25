from collections import defaultdict


class Register:
    data = defaultdict(dict)
    data["db_details"] = {}
    data["models_create"] = {}
