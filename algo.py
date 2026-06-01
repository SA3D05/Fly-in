"""Simulation logic for moving drones across the map graph.

This module contains the `Simulator` class responsible for building the
graph, computing shortest paths, and advancing simulation steps.
"""

from models import Connection, Drone, Hub, MapData
from enums import ZoneType, HubType


class Simulator:
    """Drive the state and rules of the drone simulation.

    Args:
        mapdata: The `MapData` instance representing the environment.
    """

    def __init__(self, mapdata: MapData) -> None:

        self.mapdata: MapData = mapdata
        self.graph: dict = dict()
        self.drones: list = list()
        self.paths: list = list()
        self.backward_stack: list = list()
        self.forward_stack: list = list()

    def init_path(self) -> None:
        """Compute all minimal-cost paths from start to end hubs.

        Uses a DFS-style search to enumerate paths and keeps only the
        shortest-cost routes (ties preserved).
        """
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

        if len(paths) == 0:
            raise ValueError("No path found from start to end.")

        smallest_step = min(paths, key=lambda x: x["cost"])["cost"]
        self.paths = [path["path"] for path in paths
                      if path["cost"] == smallest_step]

    def init_graph(self) -> None:
        """Build graph (adjacency list) with traversal costs.

        The cost is derived from the `ZoneType` of the destination hub.
        """
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
        """Reset simulation state and stacks."""

        for hub in self.mapdata.hubs.values():
            hub.reset()

        for c in self.mapdata.connections:
            c.reset()

        self.drones = list()
        self.init_drones()
        self.backward_stack = list()
        self.forward_stack = list()

    def __print_log(self, id: int, destination: str) -> None:
        """Print a short movement log for a drone.

        Args:
            id: Drone identifier.
            destination: Destination hub or connection description.
        """
        print(f"D{id}-{destination}", end=" ")

    def is_end(self) -> bool:
        """Return True if all drones have reached the end hub."""
        for drone in self.drones:
            if not isinstance(drone.current_station, Hub):
                return False
            if drone.current_station.hub_type != HubType.END:
                return False
        return True

    def forward(self) -> bool:
        """Advance the recorded forward state if available.

        Returns:
            True when the forward step was applied, False otherwise.
        """
        if len(self.forward_stack) < 1:
            return False
        instractions = self.forward_stack.pop()

        self.backward_stack.append(list())

        for drone, coordinates in instractions:
            self.__set_backward_state(drone)
            self.__update_drone_coordinates(drone, *coordinates)
        return True

    def backward(self) -> bool:
        """Rewind the simulation one recorded step if available.

        Returns:
            True when rewind was applied, False otherwise.
        """
        if len(self.backward_stack) < 1:
            return False
        instractions = self.backward_stack.pop()

        self.forward_stack.append(list())

        for drone, coordinates in instractions:
            self.__set_forward_state(drone)
            self.__update_drone_coordinates(drone, *coordinates)

        return True

    def __set_backward_state(self, drone: Drone) -> None:
        """Record the current drone position to the backward stack."""
        self.backward_stack[-1].append((drone, (drone.x, drone.y)))

    def __set_forward_state(self, drone: Drone) -> None:
        """Record the current drone position to the forward stack."""
        self.forward_stack[-1].append((drone, (drone.x, drone.y)))

    def __move_connection_step(self, drone: Drone, target_hub: Hub) -> None:
        """Complete a drone move from a connection into a hub.

        Args:
            drone: Drone to move.
            target_hub: Destination hub instance.
        """
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
        """Move a drone halfway into a restricted hub (enter connection).

        This places the drone on the connection and updates counters.
        """

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
        """Update drone coordinates, optionally moving halfway to target.

        Args:
            drone: Drone to update.
            targte_x: Target x coordinate.
            target_y: Target y coordinate.
            to_connection: When True, place the drone halfway between
                current position and target to represent being on a link.
        """
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
        """Perform a full move of a drone from its current station.

        Args:
            drone: Drone being moved.
            target_hub: Destination hub instance.
            current_connction: Connection used for the move.
        """

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
        """Return the `Connection` object between two hubs, if present.

        Args:
            current_hub: Source hub instance.
            target_hub: Target hub instance.

        Returns:
            The matching `Connection` or None if not found.
        """
        for c in self.mapdata.connections:
            if c.hub_from is current_hub and c.hub_to is target_hub:
                return c
            if c.hub_from is target_hub and c.hub_to is current_hub:
                return c
        return None

    def make_step(self) -> None:
        """Advance the simulation by one step for all drones.

        The method evaluates each drone and moves it along a chosen path
        when possible, recording changes for undo/redo stacks.
        """

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
        """Choose the next hub on a valid path for the given drone.

        Returns:
            The next `Hub` to move to, or None if no valid move exists.
        """
        current_station: Hub | Connection = drone.current_station

        if isinstance(current_station, Connection):
            return current_station.hub_to

        for i in range(len(self.paths)):
            try:
                hub_idx = self.paths[i].index(drone.current_station)
            except ValueError:
                continue

            path_idx = i
            targert_station = (
                self.mapdata.hubs[self.paths[path_idx][hub_idx + 1].name]
                )

            if not targert_station.can_enter():
                continue
            return targert_station

        return None

    def init_drones(self) -> None:
        """Instantiate `Drone` objects at the start hub for the map."""

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
