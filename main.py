"""Entry point for running the drone simulation.

Usage: `python main.py [config_map.txt]`
If no arguments are provided, the default map from `Config.MAP_FILE`
is used.
"""

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

if __name__ == "__main__":
    import sys
    from display import Display
    from models import MapData
    from algo import Simulator
    from parser import Parser
    import pygame
    pygame.init()
    try:
        if len(sys.argv) < 2:
            print("Error: no map file provided.")
            sys.exit()
        elif len(sys.argv) > 2:
            print("Error: too many arguments.")
            sys.exit()
        parser: Parser = Parser(sys.argv[1])
        parser.parse()

        mapdata: MapData = MapData()
        mapdata.build_obj(parser.get_raw_data())
        sim: Simulator = Simulator(mapdata)

        sim.init_graph()
        try:
            sim.init_path()
        except Exception as e:
            print(f"[Error]: {e}")
            sys.exit()
        sim.init_drones()

        display: Display = Display(sim, sys.argv[1], mapdata)

        display.game_loop()

    except BaseException:
        print("\nProgram Exit")
