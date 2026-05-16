import re
import sys

from enums import ZoneType


class Parser:
    def __get_lines(self, filename: str) -> list[str]:
        lines: list[str] = []
        try:
            with open(filename) as f:
                for line in f:
                    lines.append(line)
            return lines
        except Exception as e:
            print(f"Error Open File: {e}")
            sys.exit()

    def __validate_hubs(self, hubs: list) -> bool:
        start_count = 0
        end_count = 0
        defined_coordinates: list[tuple[int, int]] = []
        defined_names: list[str] = []

        for hub in hubs:
            if hub["type"] == "start_hub":
                start_count += 1
            elif hub["type"] == "end_hub":
                end_count += 1

            current_coordinates = (hub["x"], hub["y"])
            if current_coordinates in defined_coordinates:
                return False
            defined_coordinates.append(current_coordinates)

            if hub["name"] in defined_names:
                return False
            defined_names.append(hub["name"])

        if start_count != 1 or end_count != 1:
            return False
        return True

    def __is_hub_define(self, hubs: list, hub_from: str, hub_to: str):
        hub_from_found = False
        hub_to_found = False

        for hub in hubs:
            if hub["name"] == hub_from:
                hub_from_found = True
            elif hub["name"] == hub_to:
                hub_to_found = True
        if hub_from_found and hub_to_found:
            return True
        return False

    def __validate_line(self, line: str) -> str | None:
        number = r"(\-|\+){0,1}[0-9]+"
        name = r"[^\-\s]+"
        tag_value = r"[a-z\_]+\=([a-z]+|[0-9]+)"
        metadata = rf"( \[{tag_value}( {tag_value})*\]){{0,1}}"

        hub_pattern = rf"{name} {number} {number}{metadata}"

        start_hub_pattern = rf"^start_hub: {hub_pattern}"
        end_hub_pattern = rf"^end_hub: {hub_pattern}"
        regular_hub_pattern = rf"^hub: {hub_pattern}"

        connection_pattern = rf"^connection: {name}\-{name}{metadata}"
        nb_drones_pattern = rf"^nb_drones: {number}"

        if re.search(nb_drones_pattern, line):
            return "nb_drones"

        elif re.search(start_hub_pattern, line):
            return "start_hub"

        elif re.search(regular_hub_pattern, line):
            return "hub"

        elif re.search(end_hub_pattern, line):
            return "end_hub"

        elif re.search(connection_pattern, line):
            return "connection"

    def __remove_comment(self, line: str):

        result = ""
        comment_start = line.find("#")

        for i, character in enumerate(line):
            if i < comment_start:
                result += character
        return result

    def parse(self, filename: str) -> dict:

        lines = self.__get_lines(filename)
        line_idx: int | None = 0
        pass_first_line = False
        pass_defined_hubs = False
        result: dict = {
            "connections": [],
            "hubs": [],
            "drones_number": 0,
        }

        try:
            for line in lines:
                line_idx += 1
                if line == "\n" or line.startswith("#"):
                    continue

                if "#" in line:
                    line = self.__remove_comment(line)

                line_type: str | None = self.__validate_line(line)

                if line_type is None:
                    raise ValueError("invalide configuration")

                splitted_line: list[str] = line.split(":")
                line_content: str = splitted_line[1].strip()

                if line_type == "nb_drones":
                    if pass_first_line:
                        raise ValueError("invalide configuration")
                    pass_first_line = True
                    try:
                        result["drones_number"] = int(line_content)
                    except Exception:
                        raise ValueError("invalide configuration")

                elif line_type == "start_hub":
                    if pass_defined_hubs:
                        raise ValueError("invalide configuration")
                    pass_first_line = True
                    result["hubs"].append(self.__parse_hub(line_content))
                    result["hubs"][-1].update({"type": "start_hub"})

                elif line_type == "end_hub":
                    if pass_defined_hubs:
                        raise ValueError("invalide configuration")
                    pass_first_line = True
                    result["hubs"].append(self.__parse_hub(line_content))
                    result["hubs"][-1].update({"type": "end_hub"})

                elif line_type == "hub":
                    if pass_defined_hubs:
                        raise ValueError("invalide configuration")
                    pass_first_line = True
                    result["hubs"].append(self.__parse_hub(line_content))
                    result["hubs"][-1].update({"type": "normal_hub"})

                elif line_type == "connection":
                    pass_first_line = True
                    pass_defined_hubs = True
                    connection = self.__parse_connection(line_content)

                    if not self.__is_hub_define(
                        result["hubs"], connection["hub_from"], connection["hub_to"]
                    ):
                        raise ValueError("invalide configuration")
                    result["connections"].append(connection)

            if not self.__validate_hubs(result["hubs"]):
                line_idx = None
                raise ValueError("invalide configuration")
            return result

        except Exception as e:

            print(f"File: {filename}", end="")
            if line_idx is not None:
                print(f", line {line_idx}")
            else:
                print()

            print(f"Error: {e}")
            sys.exit()

    def __parse_hub(self, line_content: str) -> dict:
        fields = line_content.split(" ", 3)

        x = int(fields[1])
        y = int(fields[2])
        result: dict = {
            "name": fields[0],
            "x": x,
            "y": y,
            "zone": ZoneType.NORMAL,
            "color": "none",
            "max_drones": 1,
        }

        if len(fields) > 3:
            result.update(self.__parse_hub_metadata(fields[3]))

        return result

    def __parse_connection(self, line_content: str) -> dict:

        fields = line_content.split(" ")
        hubs = fields[0].split("-")

        if hubs[0] == hubs[1]:
            raise ValueError("Metadata not valid")
        result: dict = {
            "hub_from": hubs[0],
            "hub_to": hubs[1],
            "max_link_capacity": 1,
        }

        if len(fields) > 1:
            result.update(self.__parse_connection_metadata(fields[1]))
        return result

    def __parse_hub_metadata(self, metadata: str) -> dict[str, ZoneType | str | int]:

        result: dict[str, ZoneType | str | int] = {
            "zone": ZoneType.NORMAL,
            "color": "none",
            "max_drones": 1,
        }

        zone = {
            "restricted": ZoneType.RESTRICTED,
            "normal": ZoneType.NORMAL,
            "blocked": ZoneType.BLOCKED,
            "priority": ZoneType.PRIORITY,
        }
        metadata = metadata.strip("[]")

        processed: list[str] = []
        for data in metadata.split(" "):

            splitted_data = data.split("=", 2)

            tag = splitted_data[0].lower()
            value = splitted_data[1].lower()

            if tag in processed:
                raise ValueError("Metadata not valid")

            processed.append(tag)
            try:
                if tag == "color":
                    result[tag] = value
                elif tag == "zone":
                    result[tag] = zone[value]
                elif tag == "max_drones":
                    n = int(value)
                    if n < 1:
                        raise ValueError()
                    result[tag] = n

            except Exception:
                raise ValueError("Metadata not valid")

        return result

    def __parse_connection_metadata(self, metadata: str) -> dict[str, int]:

        metadata = metadata.strip("[]")
        fields = metadata.split(" ")

        if len(fields) != 1:
            raise ValueError("Metadata not valid")

        splitted_data = fields[0].split("=")

        if len(splitted_data) != 2:
            raise ValueError("Metadata not valid")

        tag: str = splitted_data[0]
        value: str = splitted_data[1]

        if tag != "max_link_capacity" or value.isdigit() == False:
            raise ValueError("Metadata not valid")

        return {
            "max_link_capacity": int(value),
        }
