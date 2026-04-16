from models import *


class Parser:

    def parse_map_file(self, filename: str) -> dict:

        result: dict = dict()
        lines: list[str] = list()
        line_idx: int = 0
        hub_id: int = 0
        connection_id: int = 0

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
                    result["drones_number"] = int(line_content)

                elif line_type == "start_hub":
                    result["start_hub"] = self.parse_hub(line_content)

                elif line_type == "end_hub":
                    result["end_hub"] = self.parse_hub(line_content)

                elif line_type == "hub":
                    hub_id += 1
                    result[f"hub-{hub_id}"] = self.parse_hub(line_content)

                elif line_type == "connection":
                    connection_id += 1
                    result[f"connection_{connection_id}"] = self.parse_connection(
                        line_content
                    )

                else:
                    raise ValueError(f"Unknown type '{line_type}'")
            return result

        except Exception as e:
            print(f"Error Parsing: {e} [line: {line_idx}]")
            exit()

    def parse_hub(self, line_content: str) -> dict:
        fields = line_content.split(" ", 3)

        try:
            x = int(fields[1])
            y = int(fields[2])
        except Exception:
            raise ValueError("Hub coordinates not valid")

        return {
            "name": fields[0],
            "x": x,
            "y": y,
            "metadata": self.parse_hub_metadata(fields[3]),
        }

    def parse_connection(self, line_content: str) -> dict:

        data_list = line_content.split(" ", 1)
        hubs = data_list[0].split("-")
        metadata: dict = {
            "max_link_capacity": 1,
        }

        if len(data_list) > 1:
            metadata["max_link_capacity"] = self.parse_connection_metadata(data_list[1])

        return {
            "hub_from": hubs[0],
            "hub_to": hubs[1],
            "metadata": metadata,
        }

    def parse_hub_metadata(self, metadata: str) -> dict:

        result: dict = {
            "zone": "normal",
            "color": "none",
            "max_drones": 1,
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

            result[tag] = value
        return result

    def parse_connection_metadata(self, metadata: str) -> int:

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

        return int(value)
