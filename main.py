import sys
from enum import Enum
from pprint import pprint


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
    orange = "orange"
    yellow = "yellow"
    cyan = "cyan"
    purple = "purple"
    brown = "brown"
    lime = "lime"
    magenta = "magenta"
    gold = "gold"
    black = "black"
    maroon = "maroon"
    darkred = "darkred"
    violet = "violet"
    crimson = "crimson"
    rainbow = "rainbow"


def valid_metadata(tag: str, value: str, connection: bool):

    PARSERS: dict = (
        {
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
                "orange": Color.orange,
                "yellow": Color.yellow,
                "cyan": Color.cyan,
                "purple": Color.purple,
                "brown": Color.brown,
                "lime": Color.lime,
                "magenta": Color.magenta,
                "gold": Color.gold,
                "black": Color.black,
                "maroon": Color.maroon,
                "darkred": Color.darkred,
                "violet": Color.violet,
                "crimson": Color.crimson,
                "rainbow": Color.rainbow,
            },
        }
        if not connection
        else {}
    )

    try:
        if tag == "max_link_capacity" and connection:
            return int(value)
        if tag == "max_drones" and not connection:
            return int(value)
        return PARSERS[tag][value]
    except Exception:
        raise ValueError(f"tag or value not valid '{tag} = {value}'")


# inpute = "[color=red test=10]".split(" ")
def parse_metadata(metadata: str, connection: bool = False) -> dict:
    result: dict = {}

    result = (
        {"max_link_capacity": 1}
        if connection
        else {
            "zone": ZoneType.Normal,
            "color": None,
            "max_drones": 1,
        }
    )

    if metadata.count("[") != 1 or metadata.count("]") != 1:
        raise ValueError("Metadata not valid")

    metadata = metadata.strip("[]")

    for data in metadata.split(" "):

        splitted_data = data.split("=")
        if len(splitted_data) != 2:
            raise ValueError("Metadata not valid")

        tag, value = splitted_data
        result.update({tag: valid_metadata(tag, value, connection)})

    return result


def parse_hub(line: str):

    result: dict = {}
    splitted_hub = line.split(":")
    fields = splitted_hub[1].strip().split(" ", 3)

    if splitted_hub[0] == "start_hub":
        result["type"] = "start_hub"

    elif splitted_hub[0] == "hub":
        result["type"] = "hub"

    elif splitted_hub[0] == "end_hub":
        result["type"] = "end_hub"

    else:
        raise ValueError(f"Hub type not valid '{fields[0]}'")

    try:
        x = int(fields[1])
        y = int(fields[2])
    except Exception:
        raise ValueError("Hub coordinates not valid")
    result.update(
        {
            "name": fields[0],
            "x": x,
            "y": y,
            "matadata": parse_metadata(fields[3]),
        }
    )
    return result


def parse_connection(line: str) -> dict:
    result: dict = {"metadata": {"max_link_capacity": 1}}
    splitted_connection = line.split(":")
    data = splitted_connection[1].strip()
    print(data, file=sys.stderr)
    data_list = data.split(" ")
    hubs = data_list[0].split("-")
    result["from"] = hubs[0]
    result["to"] = hubs[1]
    if len(data_list) > 1:
        result["metadata"] = parse_metadata(data_list[1], True)
    return result


def main():
    map_data: dict = {
        "hubs": [],
        "connections": [],
    }
    lines = []
    line_idx = 0  # line that error on
    hub_idx = 0
    connection_idx = 0

    # ================== open the file =================
    try:
        with open(sys.argv[1]) as f:
            for line in f:
                lines.append(line)
    except Exception as e:
        print(e)
    # ==================================================

    try:
        for line in lines:
            line_idx += 1

            # skip empty line or command '#'
            if line == "\n" or line.startswith("#"):
                continue

            # split
            splitted_line = line.split(":")

            if len(splitted_line) != 2:
                raise ValueError(f"Line not valid")

            if splitted_line[0] == "nb_drones":
                map_data["nb_drones"] = int(splitted_line[1].strip())

            elif "hub" in splitted_line[0]:
                map_data["hubs"].append(parse_hub(line))

            elif splitted_line[0] == "connection":
                map_data["connections"].append(parse_connection(line))
            else:
                pass  # add unkownn type error later

        pprint(map_data, sort_dicts=False)
    except Exception as e:
        print(f"Parsing error: {e} [line: {line_idx}]")
    return map_data


if __name__ == "__main__":
    main()
