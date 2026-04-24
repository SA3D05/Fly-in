from pprint import pprint

from globals import FONT_FAMILY_PATH, HUB_NAME_SIZE, HUB_SIZE
import pygame


class Connection:

    def __init__(
        self,
        hub_from: str,
        hub_to: str,
        start: tuple[int, int],
        end: tuple[int, int],
        max_link_capacity: int = 1,
    ) -> None:
        self.hub_from: str = hub_from
        self.hub_to: str = hub_to
        self.max_link_capacity: int = max_link_capacity
        self.start_pos: tuple[int, int] = start
        self.end_pos: tuple[int, int] = end


class Hub:

    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        color: str,  # later make in Color type
        max_drones: int,
        hub_type: str,  # later make in HubType type
        zone_type: str,  # later make in ZoneType type
    ) -> None:

        self.name = name
        self.x = x
        self.y = y
        self.color = color
        self.max_drones = max_drones
        self.hub_type = hub_type
        self.zone_type = zone_type

        self.surf = pygame.Surface((HUB_SIZE, HUB_SIZE))

        self.text_base = pygame.font.Font(FONT_FAMILY_PATH, HUB_NAME_SIZE)
        self.text_surf = self.text_base.render(name, True, color)

        self.surf.fill(color)
        self.to_end = 0


class MapData:
    def __init__(self) -> None:

        self.hubs: dict[str, Hub] = {}
        self.connections: list[Connection] = []

        self.start_hub: Hub | None = None
        self.end_hub: Hub | None = None
        self.drones_number: int = 0

    def get_start_hub(self) -> Hub:
        if self.start_hub is None:
            raise ValueError("Start hub cannot be None")
        return self.start_hub

    def get_end_hub(self) -> Hub:
        if self.end_hub is None:
            raise ValueError("End hub cannot be None")
        return self.end_hub

    def build_obj(self, raw_data: dict) -> None:
        self.drones_number = raw_data["drones_number"]

        for hub in raw_data["hubs"]:

            self.hubs[hub["name"]] = Hub(
                hub["name"],
                hub["x"],
                hub["y"],
                hub["color"],
                hub["max_drones"],
                hub["type"],
                hub["zone"],
            )

            if hub["type"] == "start_hub":
                self.start_hub = self.hubs[hub["name"]]
            elif hub["type"] == "end_hub":
                self.end_hub = self.hubs[hub["name"]]

        for c in raw_data["connections"]:
            self.connections.append(
                Connection(
                    c["hub_from"],
                    c["hub_to"],
                    (self.hubs[c["hub_from"]].x, self.hubs[c["hub_from"]].y),
                    (self.hubs[c["hub_to"]].x, self.hubs[c["hub_to"]].y),
                    c["max_link_capacity"],
                )
            )
        self.graph: dict = {}


class Drone:

    def __init__(
        self,
        graph: dict,
        hubs: dict[str, Hub],
        start_hub: str,
    ) -> None:

        self.hubs = hubs
        self.size = HUB_SIZE - 10
        self.surf = pygame.Surface((self.size, self.size))
        self.graph = graph
        self.current_hub: str = start_hub
        self.x = hubs[start_hub].x
        self.y = hubs[start_hub].y
        self.surf.fill("white")

    def move(self) -> None:
        target_hub: str = self.current_hub

        for hub in self.graph[self.current_hub]:
            if self.hubs[hub].to_end < self.hubs[target_hub].to_end:
                target_hub = hub
        self.current_hub = target_hub
        self.x = self.hubs[self.current_hub].x
        self.y = self.hubs[self.current_hub].y
