from models import Connection, Drone, Hub, MapData
from enums import ZoneType, HubType


class Simulator:

    def __init__(self, mapdata: MapData) -> None:

        self.mapdata: MapData = mapdata
        self.graph: dict = dict()
        self.drones: list = list()
        self.paths: list = list()
        self.backward_stack: list = list()
        self.forward_stack: list = list()

    def init_path(self) -> None:
        stack: list = [([self.mapdata.get_start_hub()], 0)]
        paths: list = []

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
        self.paths = [path["path"] for path in paths
                      if path["cost"] == smallest_step]

    def init_graph(self) -> None:
        type_cost = {
            ZoneType.NORMAL: 1,
            ZoneType.BLOCKED: -1,
            ZoneType.RESTRICTED: 2,
            ZoneType.PRIORITY: 0,
        }

        for c in self.mapdata.connections:

            self.graph.setdefault(c.hub_from, []).append(
                (c.hub_to, type_cost[c.hub_to.zone_type]),
            )

            self.graph.setdefault(c.hub_to, []).append(
                (c.hub_from, type_cost[c.hub_to.zone_type]),
            )

    def reset(self) -> None:

        for hub in self.mapdata.hubs.values():
            hub.reset()

        for c in self.mapdata.connections:
            c.reset()

        self.drones = list()
        self.init_drones()
        self.backward_stack = list()
        self.forward_stack = list()

    def __print_log(self, id: int, destination: str) -> None:
        print(f"D{id}-{destination}", end=" ")

    def is_end(self) -> bool:
        for drone in self.drones:
            if not isinstance(drone.current_station, Hub):
                return False
            if drone.current_station.hub_type != HubType.END:
                return False
        return True

    def forward(self) -> bool:
        if len(self.forward_stack) < 1:
            return False
        instractions = self.forward_stack.pop()

        self.backward_stack.append(list())

        for drone, coordinates in instractions:
            self.__set_backward_state(drone)
            self.__update_drone_coordinates(drone, *coordinates)
        return True

    def backward(self) -> bool:
        if len(self.backward_stack) < 1:
            return False
        instractions = self.backward_stack.pop()

        self.forward_stack.append(list())

        for drone, coordinates in instractions:
            self.__set_forward_state(drone)
            self.__update_drone_coordinates(drone, *coordinates)

        return True

    def __set_backward_state(self, drone: Drone) -> None:
        self.backward_stack[-1].append((drone, (drone.x, drone.y)))

    def __set_forward_state(self, drone: Drone) -> None:
        self.forward_stack[-1].append((drone, (drone.x, drone.y)))

    def __move_connection_step(self, drone: Drone, target_hub: Hub) -> None:
        target_hub.incoming_drones -= 1
        drone.current_station.leave_station()
        drone.current_station = target_hub

        self.__set_backward_state(drone)
        self.__update_drone_coordinates(
            drone,
            target_hub.x,
            target_hub.y,
        )
        self.__print_log(drone.id, target_hub.name)

    def __move_half(
        self, drone: Drone, target_hub: Hub, target_connction: Connection
    ) -> None:

        target_hub.incoming_drones += 1
        drone.current_station.leave_station()
        drone.current_station = target_connction
        drone.current_station.enter_station()

        self.__update_drone_coordinates(
            drone,
            target_hub.x,
            target_hub.y,
            True,
        )
        self.__print_log(
            drone.id,
            f"{target_connction.hub_from.name}-{target_connction.hub_to.name}",
        )

    def __update_drone_coordinates(
        self,
        drone: Drone,
        targte_x: float,
        target_y: float,
        to_connection: bool = False,
    ) -> None:

        if to_connection:
            drone.x = (drone.x + targte_x) / 2
            drone.y = (drone.y + target_y) / 2
        else:
            drone.x = targte_x
            drone.y = target_y

    def __move(
        self,
        drone: Drone,
        target_hub: Hub,
        current_connction: Connection,
    ) -> None:

        if target_hub.is_restricted():
            self.__set_backward_state(drone)
            self.__move_half(drone, target_hub, current_connction)

        else:
            drone.current_station.leave_station()
            drone.current_station = target_hub
            drone.current_station.enter_station()

            self.__set_backward_state(drone)
            self.__update_drone_coordinates(drone, target_hub.x, target_hub.y)
            self.__print_log(drone.id, target_hub.name)

    def __get_connection(
        self,
        current_hub: Hub,
        target_hub: Hub,
    ) -> Connection | None:
        for c in self.mapdata.connections:
            if c.hub_from is current_hub and c.hub_to is target_hub:
                return c
            if c.hub_from is target_hub and c.hub_to is current_hub:
                return c
        return None

    def make_step(self) -> None:

        self.backward_stack.append(list())

        for drone in self.drones:
            if (
                isinstance(drone.current_station, Hub)
                and drone.current_station.is_end_hub()
            ):
                continue

            target_station: Hub | None = self.__choose_correct_path(drone)

            if target_station is None:
                continue

            if isinstance(drone.current_station, Connection):
                self.__move_connection_step(drone, target_station)

            elif target_station.can_enter():
                target_connection = self.__get_connection(
                    drone.current_station, target_station
                )
                if (
                    target_connection is not None
                    and target_connection.can_pass()
                ):
                    self.__move(drone, target_station, target_connection)

        print()

    def __choose_correct_path(self, drone: Drone) -> Hub | None:
        current_station: Hub | Connection = drone.current_station

        if isinstance(current_station, Connection):
            return current_station.hub_to

        for i in range(len(self.paths)):
            try:
                hub_idx = self.paths[i].index(drone.current_station)
            except ValueError:
                continue

            path_idx = i
            targert_station = self.mapdata.hubs[
                self.paths[path_idx][hub_idx + 1].name
                ]

            if not targert_station.can_enter():
                continue
            return targert_station

        return None

    def init_drones(self) -> None:

        x, y = self.mapdata.get_start_hub().get_coordinates()

        for drone_id in range(self.mapdata.drones_number):
            self.drones.append(
                Drone(
                    drone_id + 1,
                    x,
                    y,
                    self.mapdata.get_start_hub(),
                )
            )
