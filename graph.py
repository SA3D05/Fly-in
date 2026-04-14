from pprint import pprint

from models import *


# start waypoint1
# waypoint1 waypoint2
# waypoint2 goal


# add mapdata and generate the graph dict to use it in algo


def to_graph(data: MapData) -> dict[str, list[str]]:
    graph: dict[str, list[str]] = {}
    for c in data.connections:
        graph.setdefault(c.hub_from, []).append(c.hub_to)
        graph.setdefault(c.hub_to, []).append(c.hub_from)

    return graph


def bfs(graph: dict[str, list[str]], first: str) -> None:

    visited: list[str] = []
    queue: list[str] = [first]
    node: str = first
    while queue:
        node = queue.pop()
        if node not in visited:
            print(node)
            visited.append(node)
            for na in graph[node]:
                queue.append(na)
