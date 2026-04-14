from pprint import pprint
from parser import Parser, MapData
import graph


from sys import argv

if __name__ == "__main__":

    parser: Parser = Parser()

    data: MapData = parser.parse_map_file(argv[1])

    graph.bfs(graph.to_graph(data), data.get_start_hub().name)
