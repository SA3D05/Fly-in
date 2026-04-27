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
                if neighbor not in path:
                    stack.append((path + [neighbor], cost + move))
        self.path = min(paths, key=lambda x: x["move"])["path"]

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

            # target_hub: Hub = self.mapdata.hubs[drone.current_hub]
            # current_hub: Hub = target_hub

            # for hub in self.graph[drone.current_hub]:
            #     current_hub = self.mapdata.hubs[hub[0]]

            #     if (
            #         current_hub.to_end < target_hub.to_end
            #         and current_hub.drones_setting == 0
            #     ) or current_hub.hub_type == "end_hub":

            #
            #         target_hub = current_hub
            #         target_hub.drones_setting += 1
            #         self.mapdata.hubs[drone.current_hub].drones_setting -= 1

            # drone.current_hub = target_hub.name
            # drone.x = target_hub.x
            # drone.y = target_hub.y

    def init_drones(self) -> None:

        start_hub: str = self.mapdata.get_start_hub().name
        coordinates: tuple[int, int] = self.mapdata.get_start_hub().get_coordinates()

        for drone_id in range(self.mapdata.drones_number):

            self.drones.append(
                Drone(
                    drone_id + 1,
                    coordinates,
                    # self.get_random_color(),
                    # "grey",
                )
            )
