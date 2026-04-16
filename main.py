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
    pygame.init()
    parser: Parser = Parser()
    map_path = "maps/easy/02_simple_fork.txt"
    data: MapData = parser.parse_map_file(map_path)
    # graph.bfs(graph.to_graph(data), data.get_start_hub().name)
    screen = display.Display(data)

    try:
        screen.game_loop()
    except BaseException:
        sys.exit()
