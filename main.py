from pprint import pprint
from parser import Parser, MapData
from graph import bfs


from sys import argv

if __name__ == "__main__":

    parser: Parser = Parser()

    data: MapData = parser.parse_map_file(argv[1])
    # bfs()
