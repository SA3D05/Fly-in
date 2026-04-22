import os
from pprint import pprint
import sys

import graph

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"


# hide pygame hello message
import pygame
from display import Display
from models import Hub, MapData
from parser import Parser
from validator import Validator
from models import ParsingError, ValidationError, Drone


if __name__ == "__main__":

    maps = [
        [
            "maps/easy/01_linear_path.txt",
            "maps/easy/02_simple_fork.txt",
            "maps/easy/03_basic_capacity.txt",
        ],
        [
            "maps/medium/01_dead_end_trap.txt",
            "maps/medium/02_circular_loop.txt",
            "maps/medium/03_priority_puzzle.txt",
        ],
        [
            "maps/hard/01_maze_nightmare.txt",
            "maps/hard/02_capacity_hell.txt",
            "maps/hard/03_ultimate_challenge.txt",
        ],
    ]

    pygame.init()
    parser: Parser = Parser()
    validator: Validator = Validator()

    try:
        raw_data: dict = parser.parse(
            maps[int(sys.argv[1]) - 1][
                int(sys.argv[2]) - 1
            ],  # just for qiuck selection
        )

        validator.validate(raw_data)
    except ValidationError as e:
        print("Validation Error:", e)
        sys.exit()
    except ParsingError as e:
        print("Parsing Error:", e)
        sys.exit()

    # validate raw_data now before passing it to pygameclea

    # json_raw_data = json.dumps(raw_data, indent=4, sort_keys=True)
    # print(json_raw_data)

    def solve(data: MapData, connections: dict, first_hub: str, to_end: int):

        stack: list[tuple[str, int]] = []
        visited: list[str] = []
        stack.append((first_hub, to_end))
        while stack:

            current_hub, to_end = stack.pop()

            data.hubs[current_hub].to_end = to_end
            visited.append(current_hub)
            to_end += 1
            for neighbor in connections[current_hub]:
                if neighbor in stack:
                    continue
                if neighbor in visited:
                    continue
                stack.append((neighbor, to_end))

    map_data: MapData = MapData()
    map_data.build_obj(raw_data)

    solve(map_data, graph.to_graph(map_data.connections), map_data.end_hub.name, 0)

    pprint({v.name: v.to_end for v in map_data.hubs.values()})

    d1 = Drone(
        map_data,
    )

    display = Display(map_data, d1)
    try:
        display.game_loop()
    except BaseException:
        sys.exit()
    # try:
    # except BaseException:
    #     sys.exit()
