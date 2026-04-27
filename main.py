#!.venv/bin/python3

import os
from pprint import pprint
from display import Display
from globals import MAP_FILE


# hide pygame hello message
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import sys
from algo import Simulator
from model import MapData
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

    # print(len(sys.argv))
    if len(sys.argv) > 1:
        MAP_FILE = maps[int(sys.argv[1]) - 1][int(sys.argv[2]) - 1]

    try:
        raw_data: dict = parser.parse(
            # just for qiuck selection
            #
            MAP_FILE
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

    sim: Simulator = Simulator(mapdata)

    sim.init_graph()
    sim.init_path()

    pprint(sim.path)
    # implement the new algo

    sim.init_drones()

    display: Display = Display(sim, MAP_FILE)

    display.game_loop()
