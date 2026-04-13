from models import *

d = Hub("w3", 0, 0, HubMetadata())
e = Hub("end", 0, 0, HubMetadata())
c = Hub("w2", 0, 0, HubMetadata())
b = Hub("w1", 0, 0, HubMetadata())
a = Hub("start", 0, 0, HubMetadata())

graph: dict = {
    a: [b],
    b: [c],
    c: [d, e],
    d: [],
    e: [],
}


def bfs(graph: dict[Hub, list[Hub]], first: Hub) -> None:

    visited: list[Hub] = []
    queue: list[Hub] = [first]
    node: Hub = first
    while queue:
        node = queue.pop()
        if node not in visited:
            print(node.name)
            visited.append(node)
            for na in graph[node]:
                queue.append(na)


bfs(graph, a)
