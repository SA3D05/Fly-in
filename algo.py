from models import Connection, Drone, Hub, HubType, MapData, ZoneType


class Simulator:

    def __init__(self, mapdata: MapData) -> None:

        self.mapdata: MapData = mapdata
        self.graph: dict[Hub, list[tuple[Hub, int]]] = {}
        self.drones: list[Drone] = []
        self.paths: list[list[Hub]] = []
        self.backward_stack: list = []
        self.forward_stack: list = []

    def init_path(self):
        stack: list[tuple] = [([self.mapdata.get_start_hub()], 0)]
        paths: list[dict] = []

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

    def reset(self):

        self.drones = []
        self.init_drones()
        self.backward_stack = []
        self.forward_stack = []

    def __print_log(self, id: int, destination: str):
        # print(f"D{id}-{destination}", end=" ")
        pass

    def is_end(self) -> bool:
        for drone in self.drones:
            if drone.current_hub.hub_type != HubType.END:
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

    def __set_backward_state(self, drone: Drone):
        self.backward_stack[-1].append((drone, (drone.x, drone.y)))

    def __set_forward_state(self, drone: Drone):
        self.forward_stack[-1].append((drone, (drone.x, drone.y)))

    def __skip_connection_step(self, drone: Drone):

        drone.in_connection = False
        drone.current_connection.drones_passing -= 1
        self.__set_backward_state(drone)
        self.__update_drone_coordinates(drone, drone.current_hub.x, drone.current_hub.y)
        self.__print_log(drone.id, drone.current_hub.name)

    def __move_half(self, drone: Drone, target_hub: Hub, current_connction: Connection):

        drone.in_connection = True
        drone.current_connection = current_connction
        current_connction.drones_passing += 1
        self.__update_drone_coordinates(
            drone, (drone.x + target_hub.x) / 2, (drone.y + target_hub.y) / 2
        )
        self.__print_log(
            drone.id,
            f"{current_connction.hub_from.name}-{current_connction.hub_to.name}",
        )

    def __update_drone_coordinates(
        self, drone: Drone, targte_x: float, target_y: float
    ):
        drone.x = targte_x
        drone.y = target_y

    def __move(
        self,
        drone: Drone,
        target_hub: Hub,
        current_connction: Connection,
    ):

        drone.current_hub.drones_setting -= 1
        target_hub.drones_setting += 1

        drone.current_hub = target_hub
        drone.current_connection = current_connction

        if target_hub.is_restricted() and drone.in_connection == False:
            self.__set_backward_state(drone)
            self.__move_half(drone, target_hub, current_connction)

        else:
            self.__set_backward_state(drone)
            self.__update_drone_coordinates(drone, target_hub.x, target_hub.y)
            self.__print_log(drone.id, target_hub.name)

    def make_step(self) -> None:

        self.backward_stack.append(list())

        for drone in self.drones:
            if drone.current_hub.hub_type == HubType.END:
                continue

            target_hub, current_connction = self.__choose_correct_path(drone)

            if drone.in_connection:
                self.__skip_connection_step(drone)
                continue

            if target_hub.can_enter() and current_connction.can_pass():
                self.__move(drone, target_hub, current_connction)

        print()

    def __choose_correct_path(self, drone: Drone) -> tuple[Hub, Connection]:
        path_idx: int = 0
        hub_idx: int = 0

        current_hub: Hub = drone.current_hub
        targert_hub: Hub = current_hub

        current_connction: Connection = drone.current_connection

        for i in range(len(self.paths)):

            try:
                hub_idx = self.paths[i].index(drone.current_hub)
            except ValueError:
                continue

            path_idx = i
            targert_hub = self.mapdata.hubs[self.paths[path_idx][hub_idx + 1].name]

            for c in self.mapdata.connections:
                if c.hub_from == current_hub and c.hub_to == targert_hub:
                    current_connction = c

            if current_connction.can_pass() == False:
                if drone.id == 2:
                    print("current_connction.can_pass():", current_connction.can_pass())
                continue
            if targert_hub.can_enter() == False:
                if drone.id == 2:
                    print(
                        "targert_hub.can_enter():",
                        targert_hub.can_enter(),
                        current_hub.name,
                    )
                continue

            break

        return (targert_hub, current_connction)

    def init_drones(self) -> None:

        x, y = self.mapdata.get_start_hub().get_coordinates()

        for drone_id in range(self.mapdata.drones_number):

            self.drones.append(
                Drone(
                    drone_id + 1,
                    self.mapdata.get_start_hub(),
                    x,
                    y,
                    self.mapdata.connections[0],
                )
            )
