import sys
from enum import Enum

map_data: dict = {
    "hub": [],
    "connection": [],
}


class ZoneType(Enum):
    Normal = "normal"
    Blocked = "blocked"
    Restricted = "restricted"
    Priority = "priority"


class Color(Enum):
    red = "red"
    blue = "blue"
    gray = "gray"
    green = "green"


def valid_metadata(tag: str, value: str):

    PARSERS = {
        "zone": {
            "normal": ZoneType.Normal,
            "blocked": ZoneType.Blocked,
            "restricted": ZoneType.Restricted,
            "priority": ZoneType.Priority,
        },
        "color": {
            "red": Color.red,
            "blue": Color.blue,
            "gray": Color.gray,
            "green": Color.green,
        },
    }

    try:
        if tag == "max_drones":
            return int(value)
        return PARSERS[tag][value]
    except KeyError:
        raise ValueError(f"tag or value not valid '{tag} = {value}'")


# inpute = "[color=red test=10]".split(" ")
def parse_metadata(metadata: str) -> dict:
    result: dict = {
        "zone": ZoneType.Normal,
        "color": None,
        "max_drones": 1,
    }
    if metadata.count("[") != 1 or metadata.count("]") != 1:
        raise ValueError("Metadata not valid")
    metadata = metadata.strip("[]")
    for data in metadata.split(" "):
        tag, value = data.split("=")
        result.update({tag: valid_metadata(tag, value)})
    return result


def parse_hub(hub_line: str):

    result: dict = {}
    fields = hub_line.split(":")
    hub_data = fields[1].split(" ")

    if fields[0] == "start_hub":
        result["type"] = "start_hub"

    elif fields[0] == "hub":
        result["type"] = "hub"

    elif fields[0] == "end_hub":
        result["type"] = "end_hub"

    result.update(
        {
            "name": hub_data[1].strip(),
            "x": int(hub_data[2]),
            "y": int(hub_data[3]),
            "matadata": parse_metadata(hub_data[4:]),
        }
    )
    return result


try:
    print(
        "a=",
        parse_metadata("[color=red zone=restricted max_drones=20]"),
        file=sys.stderr,
    )
except Exception as e:
    print("# Error Parsing:", e, file=sys.stderr)
exit()


def parse_connection(data: str) -> dict:
    result: dict = {}
    data = data.strip()
    data_list = data.split(" ")
    hubs = data_list[0].split("-")
    result["from"] = hubs[0]
    result["to"] = hubs[1]
    if len(data_list) > 1:
        result["metadata"] = parse_metadata(data_list[1:])

    return result

def main():
    lines = []
    try:
        with open(sys.argv[1]) as f:
            for line in f:
                lines.append(line)
    except Exception as e:
        print(e)


    for line in lines:
        line = line.split(":")
        if line[0] == "nb_drones":
            map_data["nb_drones"] = int(line[1].strip())
        elif "hub" in line[0]:
            pass
        elif line[0] == "connection":
            map_data["connection"].append(parse_connection(line[1]))

    print("test =", map_data, file=sys.stderr)

if 