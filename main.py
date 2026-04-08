import sys

map_data: dict = {
    "hub": [],
    "connection": [],
}


def parse_metadata(metadata: list) -> dict:
    result: dict = {}
    print("parse_metadata,", metadata)
    for data in metadata:
        stripped_data = data.strip("[]")
        splitted_data = stripped_data.split("=")
        result.update({splitted_data[0]: splitted_data[1]})
    return result


def parse_hub(hub: str):
    pass


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
        line_info = line[1].strip().split(" ")
        new_data = {
            "name": line_info[0],
            "x": int(line_info[1]),
            "y": int(line_info[2]),
            "matadata": parse_metadata(line_info[3:]),
        }
        if line[0] == "start_hub" or line[0] == "end_hub":
            map_data[line[0]] = new_data
        elif line[0] == "hub":
            map_data[line[0]].append(new_data)
    elif line[0] == "connection":

        map_data["connection"].append(parse_connection(line[1]))

print("test =", map_data, file=sys.stderr)
