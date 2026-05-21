from enums import HubType, ZoneType
import pygame
import re
import sys


class Parser:

    def __init__(self, filename: str) -> None:
        self.hubs: list = list()
        self.connections: list = list()
        self.nb_drones: int = 0
        self.filename = filename

    def __validate_color(self, color: str) -> bool:
        try:
            pygame.Color(color)
            return True
        except ValueError:
            return False

    def get_raw_data(self) -> dict:
        return {
            "nb_drones": self.nb_drones,
            "hubs": self.hubs,
            "connections": self.connections,
        }

    def __get_lines(self) -> list:
        lines: list = []
        try:
            with open(self.filename) as f:
                for line in f:
                    lines.append(line)
            return lines
        except Exception as e:
            print(f"Error Open File: {e}")
            sys.exit()

    def check_hubs_define(self, connection: dict) -> None:
        hub_from_found = False
        hub_to_found = False
        hub_from = connection["hub_from"]
        hub_to = connection["hub_to"]

        for hub in self.hubs:
            if hub["name"] == hub_from:
                hub_from_found = True
            elif hub["name"] == hub_to:
                hub_to_found = True

        if not hub_from_found:
            raise ValueError(f"hub '{hub_from}' are not define.")

        if not hub_to_found:
            raise ValueError(f"hub '{hub_to}' are not define.")

    def __remove_comment(self, line: str) -> str:
        result: str = str()
        comment_start = line.find("#")

        for i, character in enumerate(line):
            if i < comment_start:
                result += character

        return result

    def __validate_hub(self, new_hub: dict) -> None:

        for hub in self.hubs:

            if hub["type"] == HubType.START and new_hub["type"] == HubType.START:
                raise ValueError("the start_hub is alredy defined.")

            if hub["type"] == HubType.END and new_hub["type"] == HubType.END:
                raise ValueError("the end_hub is alredy defined.")

            if hub["name"] == new_hub["name"]:
                raise ValueError(
                    f"the hub name '{hub['name']}' is alredy used.",
                )

            if hub["x"] == new_hub["x"] and hub["y"] == new_hub["y"]:
                raise ValueError(
                    f"the coordinates is alredy used in '{hub['name']}'.",
                )

    def __check_start_end(self) -> None:
        start_count = 0
        end_count = 0
        for hub in self.hubs:
            if hub["type"] == HubType.START:
                start_count += 1
            elif hub["type"] == HubType.END:
                end_count += 1

        if start_count < 1:
            raise ValueError("start_hub no provided.")

        if end_count < 1:
            raise ValueError("end_hub no provided.")

    def parse(self) -> None:

        lines: list[str] = self.__get_lines()
        line_idx: int = 0

        try:
            for line in lines:
                line_idx += 1
                if line == "\n" or line.startswith("#"):
                    continue

                if "#" in line:
                    line = self.__remove_comment(line)

                splitted_line: list[str] = line.split(":")

                if len(splitted_line) != 2:
                    raise ValueError("invalid configuration.")

                if re.search(r"^.+: .+$", line) is None:
                    raise ValueError("invalid configuration.")

                line_type: str = splitted_line[0]
                line_content: str = splitted_line[1].strip()

                if line_type == "nb_drones":
                    self.__parse_nb_drones(line_content)
                elif "hub" in line_type:
                    self.__parse_hub(line_content, line_type)

                elif line_type == "connection":
                    self.__parse_connection(line_content)

                else:
                    raise ValueError(f"unknown type '{line_type}'")

            self.__check_start_end()

        except Exception as e:
            print(f"File: {self.filename}", end="")
            if line_idx is not None:
                print(f", line {line_idx}")
            else:
                print()

            print(f"Error: {e}")
            # print()
            # pprint(self.__dict__)
            exit()

    def __parse_nb_drones(self, line_content: str) -> None:

        if re.search(r"^(\+|\-){0,1}[0-9]+$", line_content) is None:
            raise ValueError("invalid configuration.")

        if int(line_content) < 1:
            raise ValueError("drones number must be a positive integer.")

        self.nb_drones = int(line_content)

    def __parse_hub(self, line_content: str, hub_type: str) -> None:

        fields = line_content.split(" ", 3)

        if len(fields) < 3:
            raise ValueError("configuration are not completed.")

        name = fields[0]

        if "-" in name:
            raise ValueError(f"names can't contain dashes '{name}'.")

        try:
            x = int(fields[1])
            y = int(fields[2])
        except Exception:
            raise ValueError("invalid coordinates.")

        new_hub = {
            "name": name,
            "x": x,
            "y": y,
            "zone": ZoneType.NORMAL,
            "color": "none",
            "max_drones": 1,
        }

        if len(fields) == 4:
            new_hub.update(self.__parse_hub_metadata(fields[3]))

        if hub_type == "start_hub":
            new_hub.update({"type": HubType.START})

        elif hub_type == "hub":
            new_hub.update({"type": HubType.NORMAL})

        elif hub_type == "end_hub":
            new_hub.update({"type": HubType.END})

        else:
            raise ValueError("invalid type.")

        self.__validate_hub(new_hub)
        self.hubs.append(new_hub)

    def __parse_connection(self, line_content: str) -> None:

        data_list = line_content.split(" ", 1)

        if data_list[0].count("-") != 1:
            raise ValueError("invalid connection configuration.")

        hub_from, hub_to = data_list[0].split("-")
        if hub_from == hub_to:
            raise ValueError("hub_from and hub_to can't be the same.")
        new_connection = {
            "hub_from": hub_from,
            "hub_to": hub_to,
            "max_link_capacity": 1,
        }

        if len(data_list) > 1:
            new_connection.update(
                self.__parse_connection_metadata(
                    data_list[1],
                )
            )

        self.check_hubs_define(new_connection)
        self.__check_connection_define(new_connection)
        self.connections.append(new_connection)

    def __check_connection_define(self, new_connection: dict) -> None:

        for connection in self.connections:
            if (
                connection["hub_from"] == new_connection["hub_from"]
                and connection["hub_to"] == new_connection["hub_to"]
            ):
                raise ValueError("the connection is alredy define.")
            if (
                connection["hub_from"] == new_connection["hub_to"]
                and connection["hub_to"] == new_connection["hub_from"]
            ):
                raise ValueError("the connection is alredy define.")

    def __parse_hub_metadata(self, metadata: str) -> dict:

        if re.search(r"^\[\w+=\w+( \w+=\w+)*\]$", metadata) is None:
            raise ValueError("invalid metadata.")

        result: dict[str, ZoneType | str | int] = {}

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

            key = splitted_data[0].lower()
            value = splitted_data[1].lower()

            if key in processed:
                raise ValueError(f"the key '{key}' alredy defined.")
            processed.append(key)

            try:
                if key == "color":
                    if value.isdigit():
                        raise ValueError(
                            "'color' value must be a"
                            "valid single-word strings."
                        )
                    if value != "rainbow" and not self.__validate_color(value):
                        raise ValueError("invalid 'color' value.")
                    result[key] = value

                elif key == "zone":
                    result[key] = zone[value]

                elif key == "max_drones":

                    if not value.isdigit() or int(value) < 1:
                        raise ValueError(
                            "'max_drones' value must be a positive integers."
                        )
                    result[key] = int(value)

                else:
                    raise ValueError(f"unknown key '{key}' in metadata.")

            except KeyError:
                raise ValueError(f"unknown value '{value}' for '{key}'.")

        return result

    def __parse_connection_metadata(self, metadata: str) -> dict:

        if metadata.count("[") != 1 or metadata.count("]") != 1:
            raise ValueError("invalid metadata.")

        metadata = metadata.strip("[]")
        data_list = metadata.split(" ")

        if len(data_list) != 1:
            raise ValueError("invalid metadata.")

        splitted_data = data_list[0].split("=")

        if len(splitted_data) != 2:
            raise ValueError("invalid metadata.")

        key: str = splitted_data[0]
        value: str = splitted_data[1]

        if key != "max_link_capacity":
            raise ValueError(f"unknown key '{key}' in metadata.")

        if not value.isdigit() or int(value) < 1:
            raise ValueError(
                "'max_link_capacity' value must be a positive integer.",
            )

        return {
            "max_link_capacity": int(value),
        }
