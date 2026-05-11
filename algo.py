from pprint import pprint
import random
import sys

from model import Connection, Drone, Hub, HubType, MapData, ZoneType


class Simulator:

    def __init__(self, mapdata: MapData) -> None:

        self.mapdata: MapData = mapdata
        self.graph: dict[Hub, list[tuple[Hub, int]]] = {}
        self.drones: list[Drone] = []
        self.paths: list[list[str]] = []

    def init_path(self):
        # implement dfs
        stack: list[tuple[list[Hub], int]] = [([self.mapdata.get_start_hub()], 0)]
        paths = []

        while stack:

            path, move = stack.pop()
            current_hub: Hub = path[-1]

            if current_hub.hub_type == HubType.END:

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
        print("path found", len(self.paths))

    def init_graph(self) -> None:
        type_cost = {
            ZoneType.NORMAL: 1,
            ZoneType.BLOCKED: -1,
            ZoneType.RESTRICTED: 2,
            ZoneType.PRIORITY: 0,
        }

        for c in self.mapdata.connections:
            self.graph.setdefault(c.hub_from, []).append(
                (
                    c.hub_to,
                    type_cost[self.mapdata.hubs[c.hub_to.name].zone_type],
                ),
            )
            self.graph.setdefault(c.hub_to, []).append(
                (
                    c.hub_from,
                    type_cost[self.mapdata.hubs[c.hub_from.name].zone_type],
                ),
            )

    def print_log(self, id: int, destination: str):
        print(f"D{id}-{destination}", end=" ", file=sys.stderr)

    def move(self, step: int = 0) -> None:

        for drone in self.drones:

            path_idx: int = 0
            hub_idx: int = 0

            current_hub: Hub = drone.current_hub
            targert_hub: Hub = current_hub

            current_connction: Connection | None = drone.current_connection

            if current_hub.hub_type == "end_hub":
                continue

            for i in range(len(self.paths)):

                try:
                    hub_idx = self.paths[i].index(drone.current_hub.name)
                except ValueError:
                    continue

                path_idx = i
                current_hub = self.mapdata.hubs[self.paths[path_idx][hub_idx]]
                targert_hub = self.mapdata.hubs[self.paths[path_idx][hub_idx + 1]]

                for c in self.mapdata.connections:
                    if c.hub_from == current_hub.name and c.hub_to == targert_hub.name:
                        current_connction = c

                if targert_hub.can_enter() == False:
                    continue
                if (
                    current_connction is not None
                    and current_connction.can_drone_pass() == False
                ):
                    continue
                break

            if drone.in_connection == True:

                drone.in_connection = False
                drone.x = current_hub.x
                drone.y = current_hub.y
                if drone.current_connection is not None:
                    drone.current_connection.drones_passing -= 1
                continue

            if (
                targert_hub.can_enter()
                and current_connction is not None
                and current_connction.can_drone_pass()
            ):

                current_hub.drones_setting -= 1
                targert_hub.drones_setting += 1

                drone.current_hub = targert_hub
                drone.current_connection = current_connction

                if targert_hub.is_restricted() and drone.in_connection == False:

                    drone.in_connection = True
                    drone.current_connection = current_connction
                    current_connction.drones_passing += 1
                    drone.x = (drone.x + targert_hub.x) / 2
                    drone.y = (drone.y + targert_hub.y) / 2
                    if current_connction is not None:
                        self.print_log(
                            drone.id,
                            f"{current_connction.hub_from}-{current_connction.hub_to}",
                        )

                else:
                    drone.x = targert_hub.x
                    drone.y = targert_hub.y

                    self.print_log(drone.id, targert_hub.name)

        print("", file=sys.stderr)

    def init_drones(self) -> None:

        coordinates: tuple[int, int] = self.mapdata.get_start_hub().get_coordinates()

        for drone_id in range(self.mapdata.drones_number):

            self.drones.append(
                Drone(
                    drone_id + 1,
                    self.mapdata.get_start_hub(),
                    coordinates,
                )
            )
