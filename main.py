import os
from pprint import pprint
import sys

import graph

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"


# hide pygame hello message
import pygame
from display import Display
from models import MapData
from parser import Parser
from validator import Validator
from models import ParsingError, ValidationError


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
    # validate raw_data now before passing it to pygame

    # json_raw_data = json.dumps(raw_data, indent=4, sort_keys=True)
    # print(json_raw_data)

    map_data: MapData = MapData()
    map_data.build_obj(raw_data)

    # pprint(raw_data)
    # print("=" * 100)
    display = Display(map_data)
    # graph.bfs(graph.to_graph(data), data.get_start_hub().name)

    try:
        display.game_loop()
    except BaseException:
        sys.exit()
