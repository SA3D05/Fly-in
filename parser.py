from models import *


class Parser:

    def parse_map_file(self, filename: str) -> MapData:

        result: MapData = MapData()
        lines: list[str] = []
        line_idx: int = 0

        try:
            with open(filename) as f:
                for line in f:
                    lines.append(line)
        except Exception as e:
            print(f"Error Open File: {e}")
            exit()

        try:
            for line in lines:
                line_idx += 1

                if line == "\n" or line.startswith("#"):
                    continue

                splitted_line: list[str] = line.split(":")
                line_type: str = splitted_line[0].strip()
                line_content: str = splitted_line[1].strip()
                if len(splitted_line) != 2:
                    raise ValueError(f"Line not valid")

                if line_type == "nb_drones":
                    result.drones_number = int(line_content)

                elif line_type == "start_hub":
                    hub: Hub = self.parse_hub(line_content)
                    result.start_hub = hub
                    result.hubs[hub.name] = hub

                elif line_type == "end_hub":
                    hub: Hub = self.parse_hub(line_content)
                    result.end_hub = self.parse_hub(line_content)
                    result.hubs[hub.name] = hub

                elif line_type == "hub":
                    hub: Hub = self.parse_hub(line_content)
                    result.hubs[hub.name] = hub

                elif line_type == "connection":
                    result.connections.append(self.parse_connection(line_content))

                else:
                    raise ValueError(f"Unknown type '{line_type}'")
            if result.start_hub is None or result.end_hub is None:
                raise ValueError("Start hub or End hub are not provided")
            return result

        except Exception as e:
            print(f"Error Parsing: {e} [line: {line_idx}]")
            exit()

    def parse_hub(self, line_content: str) -> Hub:
        fields = line_content.split(" ", 3)

        try:
            x = int(fields[1])
            y = int(fields[2])
        except Exception:
            raise ValueError("Hub coordinates not valid")

        return Hub(fields[0], x, y, self.parse_hub_metadata(fields[3]))

    def parse_connection(self, line_content: str) -> Connection:

        data_list = line_content.split(" ", 1)
        hubs = data_list[0].split("-")
        hub_from: str = hubs[0]
        hub_to: str = hubs[1]
        metadata: ConnectionMetadata = ConnectionMetadata()

        if len(data_list) > 1:
            metadata = self.parse_connection_metadata(data_list[1])

        return Connection(hub_from, hub_to, metadata)

    def parse_hub_metadata(self, metadata: str) -> HubMetadata:

        result: HubMetadata = HubMetadata()

        parsers = {
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

        if metadata.count("[") != 1 or metadata.count("]") != 1:
            raise ValueError("Metadata not valid")

        metadata = metadata.strip("[]")

        for data in metadata.split(" "):

            splitted_data = data.split("=")
            if len(splitted_data) != 2:
                raise ValueError("Metadata not valid")

            tag: str = splitted_data[0]
            value: str = splitted_data[1]
            try:
                match tag:
                    case "zone":
                        result.zone = parsers[tag][value]
                    case "color":
                        result.color = parsers[tag][value]
                    case "max_drones":
                        result.max_drones = int(value)
            except Exception as e:
                raise ValueError("Metadata not valid")

        return result

    def parse_connection_metadata(self, metadata: str) -> ConnectionMetadata:

        result: ConnectionMetadata = ConnectionMetadata()
        if metadata.count("[") != 1 or metadata.count("]") != 1:
            raise ValueError("Metadata not valid")

        metadata = metadata.strip("[]")
        data_list = metadata.split(" ")

        if len(data_list) != 1:
            raise ValueError("Metadata not valid")

        splitted_data = data_list[0].split("=")
        if len(splitted_data) != 2:
            raise ValueError("Metadata not valid")

        tag: str = splitted_data[0]
        value: str = splitted_data[1]

        if tag != "max_link_capacity":
            raise ValueError("Metadata not valid")

        result.max_link_capacity = int(value)

        return result
