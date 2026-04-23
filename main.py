#!.venv/bin/python3

import os


# hide pygame hello message
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import sys
from pprint import pprint
from algo import to_graph
from display import Display
from model import Drone, MapData
from parser import Parser
from validator import Validator
from exception_modles import ParsingError, ValidationError


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
            maps[int(sys.argv[1]) - 1][int(sys.argv[2]) - 1]  # just for qiuck selection
        )

        validator.validate(raw_data)
    except ValidationError as e:
        print("Validation Error:", e)
        sys.exit()
    except ParsingError as e:
        print("Parsing Error:", e)
        sys.exit()

    mapdata: MapData = MapData()
    mapdata.build_obj(raw_data)
    mapdata.graph = to_graph(mapdata.connections)

    # solve(mapdata, graph.to_graph(mapdata.connections), mapdata.end_hub.name, 0)

    pprint({v.name: v.to_end for v in mapdata.hubs.values()})

    d1 = Drone(mapdata)
    display = Display(mapdata, d1)
    display.game_loop()

    # try:
    #     display.game_loop()
    # except BaseException:
    #     sys.exit()
    # try:
    # except BaseException:
    #     sys.exit()
