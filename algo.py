from model import MapData


class Simulator:

    def __init__(self, mapdata: MapData) -> None:
        self.mapdata = mapdata
        self.graph: dict[str, list[str]] = {}

    def solve(self) -> None:

        stack: list[tuple[str, int]] = []
        visited: list[str] = []
        stack.append((self.mapdata.get_end_hub().name, 0))

        while stack:
            current_hub, to_end = stack.pop()
            self.mapdata.hubs[current_hub].to_end = to_end
            visited.append(current_hub)
            to_end += 1
            for neighbor in self.graph[current_hub]:
                if neighbor in stack:
                    continue
                if neighbor in visited:
                    continue
                stack.append((neighbor, to_end))

    def generate_graph(self) -> None:
        for c in self.mapdata.connections:
            self.graph.setdefault(c.hub_from, []).append(c.hub_to)
            self.graph.setdefault(c.hub_to, []).append(c.hub_from)


# def bfs(graph: dict[str, list[str]], first: str) -> None:

#     visited: list[str] = []
#     queue: list[str] = [first]
#     node: str = first
#     while queue:
#         node = queue.pop()
#         if node not in visited:
#             print(node)
#             visited.append(node)
#             for na in graph[node]:
#                 queue.append(na)
