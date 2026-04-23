from model import Connection, MapData


def solve(data: MapData, graph: dict, first_hub: str, to_end: int):

    stack: list[tuple[str, int]] = []
    visited: list[str] = []
    stack.append((first_hub, to_end))
    while stack:

        current_hub, to_end = stack.pop()

        data.hubs[current_hub].to_end = to_end
        visited.append(current_hub)
        to_end += 1
        for neighbor in graph[current_hub]:
            if neighbor in stack:
                continue
            if neighbor in visited:
                continue
            stack.append((neighbor, to_end))


def to_graph(connections: list[Connection]) -> dict[str, list[str]]:
    graph: dict[str, list[str]] = {}
    for c in connections:
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
