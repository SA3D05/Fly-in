from pprint import pprint
import random

from model import Drone, Hub, MapData


class Simulator:

    def __init__(self, mapdata: MapData) -> None:

        self.mapdata: MapData = mapdata
        self.graph: dict[str, list[tuple[str, int]]] = {}
        self.drones: list[Drone] = []

    def get_random_color(self) -> tuple:
        return tuple(random.randint(0, 255) for _ in range(3))

    def solve(self) -> None:
        stack: list[tuple[str, int]] = [
            (self.mapdata.get_end_hub().name, 0),
        ]
        visited: list[str] = []

        while stack:

            current_hub, to_end = stack.pop()
            print(current_hub, to_end)
            self.mapdata.hubs[current_hub].to_end = to_end
            visited.append(current_hub)
            # to_end += 1
            for neighbor, cost in self.graph[current_hub]:
                if neighbor in stack:
                    continue
                if neighbor in visited:
                    continue
                stack.append((neighbor, to_end + cost))

        # pprint({h.name: h.to_end for h in self.mapdata.hubs.values()})

    def new_solve(self):
        # implement dfs
        stack = [([self.mapdata.get_start_hub().name], 0)]

        paths = []
        while stack:

            print(stack)
            input()
            path, move = stack.pop()
            current_hub = path[-1]

            if current_hub == "goal":
                paths.append(
                    {
                        "move": move,
                        "path": path,
                    }
                )
                continue
            for neighbor, cost in self.graph[current_hub]:
                if neighbor not in path:
                    stack.append((path + [neighbor], cost + move))
        print(paths)

    # p = {
    # start : [dist_gate1]
    # dist_gate1:[start]

    # }
    def init_graph(self) -> None:
        # pprint([c.__dict__ for c in self.mapdata.connections])
        cost = {
            "normal": 1,
            "blocked": -1,
            "restricted": 2,
            "priority": 1,
        }
        for c in self.mapdata.connections:
            self.graph.setdefault(c.hub_from, []).append(
                (
                    c.hub_to,
                    cost[self.mapdata.hubs[c.hub_to].zone_type],
                ),
            )
            self.graph.setdefault(c.hub_to, []).append(
                (
                    c.hub_from,
                    cost[self.mapdata.hubs[c.hub_from].zone_type],
                ),
            )
        pprint(self.graph)

    def move(self, move: int) -> None:
        print("=" * 10, "move", move, "=" * 10)
        for drone in self.drones:

            if drone.reach_goal:
                continue

            target_hub: Hub = self.mapdata.hubs[drone.current_hub]
            current_hub: Hub = target_hub

            for hub in self.graph[drone.current_hub]:
                current_hub = self.mapdata.hubs[hub[0]]

                if (
                    current_hub.to_end < target_hub.to_end
                    and current_hub.drones_setting == 0
                ) or current_hub.hub_type == "end_hub":

                    print(
                        f"Drone '{drone.id}'",
                        f"go from '{drone.current_hub}'",
                        f"to '{current_hub.name}'",
                    )

                    target_hub = current_hub
                    target_hub.drones_setting += 1
                    self.mapdata.hubs[drone.current_hub].drones_setting -= 1

            drone.current_hub = target_hub.name
            drone.x = target_hub.x
            drone.y = target_hub.y

    def init_drones(self) -> None:

        start_hub: str = self.mapdata.get_start_hub().name
        coordinates: tuple[int, int] = self.mapdata.get_start_hub().get_coordinates()

        for drone_id in range(self.mapdata.drones_number):

            self.drones.append(
                Drone(
                    drone_id + 1,
                    coordinates,
                    start_hub,
                    # self.get_random_color(),
                    # "grey",
                )
            )
