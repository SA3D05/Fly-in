import sys
from enum import Enum


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
        splitted_data = data.split("=")
        if len(splitted_data) != 2:
            raise ValueError("Metadata not valid")
        tag, value = splitted_data
        result.update({tag: valid_metadata(tag, value)})
    return result


def parse_hub(hub_line: str):

    print(hub_line)
    result: dict = {}
    hub_data = hub_line.split(":")
    fields = hub_data[1].strip().split(" ", 3)

    if hub_data[0] == "start_hub":
        result["type"] = "start_hub"

    elif hub_data[0] == "hub":
        result["type"] = "hub"

    elif hub_data[0] == "end_hub":
        result["type"] = "end_hub"

    else:
        raise ValueError(f"Hub type not valid '{fields[0]}'")

    x = fields[1]
    y = fields[2]

    if not x.isdecimal() or not y.isdecimal():
        raise ValueError(f"Hub not valid")
    result.update(
        {
            "name": fields[0],
            "x": int(x),
            "y": int(y),
            "matadata": parse_metadata(fields[3]),
        }
    )
    print("OK:", result)
    return result


def parse_connection(data: str) -> dict:
    result: dict = {}
    data = data.strip()
    data_list = data.split(" ")
    hubs = data_list[0].split("-")
    result["from"] = hubs[0]
    result["to"] = hubs[1]
    if len(data_list) > 1:
        result["metadata"] = parse_metadata(data_list[1])

    return result


def main():
    map_data = {}
    lines = []
    error_number = 0
    try:
        with open(sys.argv[1]) as f:
            for line in f:
                lines.append(line)
    except Exception as e:
        print(e)

    try:
        for i, line in enumerate(lines):
            print(line)
            if line == "\n" or line.startswith("#"):
                continue
            error_number = i + 1
            splitted_line = line.split(":")

            if len(splitted_line) != 2:
                raise ValueError(f"Line not valid")

            if splitted_line[0] == "nb_drones":
                map_data["nb_drones"] = int(splitted_line[1].strip())

            elif "hub" in splitted_line[0]:
                map_data[f"hub_{i + 1}"] = parse_hub(line)

            # elif line[0] == "connection":
            #     map_data["connection"].append(parse_connection(line))
            else:
                pass  # add unkownn type error later
        print("a=", map_data, file=sys.stderr)
    except Exception as e:
        print(f"Parsing error: {e} [line: {error_number}]")
    return map_data


if __name__ == "__main__":
    main()
