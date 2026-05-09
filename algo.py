from pprint import pprint
import random

from model import Drone, Hub, MapData


class Simulator:

    def __init__(self, mapdata: MapData) -> None:

        self.mapdata: MapData = mapdata
        self.graph: dict[str, list[tuple[str, int]]] = {}
        self.drones: list[Drone] = []
        self.paths: list[list[str]] = []

    def init_path(self, start: str):
        # implement dfs
        stack = [([start], 0)]
        paths = []

        while stack:

            path, move = stack.pop()
            current_hub = path[-1]

            if current_hub == "goal":

                paths.append(
                    {
                        "cost": move,
                        "path": path,
                    }
                )
                continue

            for neighbor, cost in self.graph[current_hub]:

                if neighbor not in path and cost != -1:
                    stack.append((path + [neighbor], cost + move))

        smallest_step = min(paths, key=lambda x: x["cost"])["cost"]

        self.paths = [path["path"] for path in paths if path["cost"] == smallest_step]
        print("Paths found", len(self.paths))
        pprint(self.paths)

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

            path_idx = 0
            hub_idx = 0
            current_hub = drone.current_hub
            next_hub = drone.current_hub

            if current_hub == "goal":
                continue

            for i in range(len(self.paths)):
                try:
                    hub_idx = self.paths[i].index(current_hub)
                except ValueError:
                    continue

                path_idx = i
                current_hub = self.paths[path_idx][hub_idx]
                next_hub = self.paths[path_idx][hub_idx + 1]

                if self.mapdata.hubs[next_hub].can_enter == False:
                    continue
                else:
                    break

            if drone.in_connection == True:
                drone.in_connection = False
                self.mapdata.hubs[current_hub].can_enter = True

                drone.x = self.mapdata.hubs[current_hub].x
                drone.y = self.mapdata.hubs[current_hub].y

                continue

            if self.mapdata.hubs[next_hub].can_enter == True or next_hub == "goal":
                print(
                    f"Drone '{drone.id}'",
                    f"go from '{current_hub}'",
                    f"to '{next_hub}'",
                )

                next_hub_x = self.mapdata.hubs[next_hub].x
                next_hub_y = self.mapdata.hubs[next_hub].y

                if (
                    self.mapdata.hubs[next_hub].zone_type == "restricted"
                    and drone.in_connection == False
                ):
                    drone.in_connection = True
                    next_hub_x = (drone.x + next_hub_x) / 2
                    next_hub_y = (drone.y + next_hub_y) / 2

                self.mapdata.hubs[next_hub].can_enter = False
                self.mapdata.hubs[current_hub].can_enter = True

                drone.current_hub = next_hub

                drone.x = next_hub_x
                drone.y = next_hub_y

    def init_drones(self) -> None:

        coordinates: tuple[int, int] = self.mapdata.get_start_hub().get_coordinates()

        for drone_id in range(self.mapdata.drones_number):

            self.drones.append(
                Drone(
                    drone_id + 1,
                    self.mapdata.get_start_hub().name,
                    coordinates,
                )
            )
