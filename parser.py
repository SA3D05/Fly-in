import re
import sys


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

    def __validate(self, line: str) -> str | None:
        number = r"(\-|\+){,1}[0-9]+"

        name = r"[^\-\s]+"
        kv = r"[a-z\_]+\=([a-z]+|[0-9]+)"
        metadata = rf"(\[{kv}(\s{kv})*\]){{,1}}"

        hub_pattern = rf"\s{name}\s{number}\s{number}\s{metadata}"

        start_hub_pattern = rf"^start_hub:{hub_pattern}"
        end_hub_pattern = rf"^end_hub:{hub_pattern}"
        regular_hub_pattern = rf"^hub:{hub_pattern}"

        connection_pattern = rf"^connection:\s{name}\-{name}\s{metadata}"
        nb_drones_pattern = rf"^nb_drones:\s{number}"

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
        line_idx: int = 0
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

                line_type: str | None = self.__validate(line)

                if line_type is None:
                    raise ValueError("invalide configuration")

                splitted_line: list[str] = line.split(":")
                line_content: str = splitted_line[1].strip()

                if line_type == "nb_drones":
                    result["drones_number"] = int(line_content)

                elif line_type == "start_hub":
                    result["hubs"].append(self.__parse_hub(line_content))
                    result["hubs"][-1].update({"type": "start_hub"})

                elif line_type == "end_hub":
                    result["hubs"].append(self.__parse_hub(line_content))
                    result["hubs"][-1].update({"type": "end_hub"})

                elif line_type == "hub":
                    result["hubs"].append(self.__parse_hub(line_content))
                    result["hubs"][-1].update({"type": "normal_hub"})

                elif line_type == "connection":
                    result["connections"].append(self.__parse_connection(line_content))

                else:
                    raise ValueError()
            return result

        except Exception as e:
            print(f"File: {filename}, line {line_idx}")
            print(f"Parsing error: {e}")
            sys.exit()

    def __parse_hub(self, line_content: str) -> dict:
        fields = line_content.split(" ", 3)

        x = int(fields[1])
        y = int(fields[2])
        result: dict = {
            "name": fields[0],
            "x": x,
            "y": y,
        }

        result.update(self.__parse_hub_metadata(fields[3]))
        return result

    def __parse_connection(self, line_content: str) -> dict:

        data_list = line_content.split(" ", 1)
        hubs = line_content.split("-")
        result: dict = {
            "hub_from": hubs[0],
            "hub_to": hubs[1],
            "max_link_capacity": 1,
        }

        if len(data_list) > 1:
            result.update(self.__parse_connection_metadata(data_list[1]))

        return result

    def __parse_hub_metadata(self, metadata: str) -> dict:

        result: dict = {
            "zone": "normal",
            "color": "none",
            "max_drones": 1,
        }
        metadata = metadata.strip("[]")

        for data in metadata.split(" "):

            splitted_data = data.split("=")
            if len(splitted_data) != 2:
                raise ValueError("Metadata not valid")

            tag: str = splitted_data[0]
            value: str = splitted_data[1]

            result[tag] = value
        return result

    def __parse_connection_metadata(self, metadata: str) -> dict:

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

        return {
            "max_link_capacity": int(value),
        }
