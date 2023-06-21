import re
import importlib


def json_to_obj(Dataclass, json_data):
    annotations = Dataclass.__dict__["__annotations__"]
    kwargs = {}

    for attr in annotations:
        if annotations[attr] == str:
            kwargs[attr] = json_data.get(attr, None)
        elif annotations[attr] == int:
            kwargs[attr] = json_data.get(attr, None)
        elif annotations[attr] == list[str] or annotations[attr] == list[int]:
            kwargs[attr] = json_data.get(attr, None)
        else:
            pattern = re.compile(r"[\w]+")
            path = pattern.findall(str(annotations[attr]))

            module = importlib.import_module(path[-2])
            NewDataclass = getattr(module, path[-1])

            if path[0] == "list":
                values = json_data if type(json_data) == list else json_data.get(attr, [])
                kwargs[attr] = [
                    json_to_obj(NewDataclass, new_json_data)
                    for new_json_data in values
                ]
            elif path[0] == "class":
                values = json_data.get(attr, None)
                kwargs[attr] = json_to_obj(
                    NewDataclass, json_data if values is None else values
                )

    return Dataclass(**kwargs)
