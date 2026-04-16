import os
from pprint import pprint
import sys

# hide pygame hello message
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame
from parser import Parser, MapData
import graph
import display

from sys import argv

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

    data: dict = parser.parse_map_file(
        maps[int(sys.argv[1]) - 1][int(sys.argv[2]) - 1],
    )

    # validate data now before passing it to pygame

    pprint(data)
    # graph.bfs(graph.to_graph(data), data.get_start_hub().name)
    # screen = display.Display(data)

    # try:
    #     screen.game_loop()
    # except BaseException:
    #     sys.exit()
