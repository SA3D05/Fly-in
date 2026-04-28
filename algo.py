from pprint import pprint
import random

from model import Drone, Hub, MapData


class Simulator:

    def __init__(self, mapdata: MapData) -> None:

        self.mapdata: MapData = mapdata
        self.graph: dict[str, list[tuple[str, int]]] = {}
        self.drones: list[Drone] = []
        self.path = []

    def init_path(self):
        # implement dfs
        stack = [([self.mapdata.get_start_hub().name], 0)]
        paths = []

        while stack:

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

                if neighbor not in path and cost != -1:
                    stack.append((path + [neighbor], cost + move))

        self.path = min(paths, key=lambda x: x["move"])["path"]

    def init_graph(self) -> None:
        type_cost = {
            "normal": 1,
            "blocked": -1,
            "restricted": 2,
            "priority": 0,
        }

        for c in self.mapdata.connections:
            self.graph.setdefault(c.hub_from, []).append(
                (
                    c.hub_to,
                    type_cost[self.mapdata.hubs[c.hub_to].zone_type],
                ),
            )
            self.graph.setdefault(c.hub_to, []).append(
                (
                    c.hub_from,
                    type_cost[self.mapdata.hubs[c.hub_from].zone_type],
                ),
            )

    def move(self, move: int) -> None:
        print("=" * 10, "move", move, "=" * 10)

        for drone in self.drones:

            current_hub = self.path[drone.path_idx]
            if current_hub == "goal":
                continue

            next_hub = self.path[drone.path_idx + 1]

            if self.mapdata.hubs[next_hub].drones_setting == 0 or next_hub == "goal":
                print(
                    f"Drone '{drone.id}'",
                    f"go from '{current_hub}'",
                    f"to '{next_hub}'",
                )

                self.mapdata.hubs[next_hub].drones_setting += 1
                self.mapdata.hubs[current_hub].drones_setting -= 1
                drone.path_idx += 1

                drone.x = self.mapdata.hubs[next_hub].x
                drone.y = self.mapdata.hubs[next_hub].y

    def init_drones(self) -> None:

        start_hub: str = self.mapdata.get_start_hub().name
        coordinates: tuple[int, int] = self.mapdata.get_start_hub().get_coordinates()

        for drone_id in range(self.mapdata.drones_number):

            self.drones.append(
                Drone(
                    drone_id + 1,
                    coordinates,
                )
            )
