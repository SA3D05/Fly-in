from enums import Config
from display import Display
import pygame
import sys
from algo import Simulator
from models import MapData
from parser import Parser

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

    try:
        pygame.init()
        file = Config.MAP_FILE.value
        if len(sys.argv) > 1:
            file = maps[int(sys.argv[1]) - 1][int(sys.argv[2]) - 1]

        parser: Parser = Parser(file)
        parser.parse()

        mapdata: MapData = MapData()
        mapdata.build_obj(parser.get_raw_data())
        sim: Simulator = Simulator(mapdata)

        sim.init_graph()
        sim.init_path()
        sim.init_drones()

        display: Display = Display(sim, file, mapdata)

        display.game_loop()

    except BaseException:
        print("\nProgram Exit")
