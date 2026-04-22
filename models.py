from enum import Enum
import os
from pprint import pprint

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame

import graph


class ParsingError(Exception): ...


class ValidationError(Exception): ...


class ZoneType(Enum):
    Normal = "normal"
    Blocked = "blocked"
    Restricted = "restricted"
    Priority = "priority"


class HubType(Enum):
    START = "start_hub"
    NORMAL = "normal_hub"
    END = "end_hub"


class Color(Enum):
    red = "red"
    blue = "blue"
    gray = "gray"
    green = "green"
    orange = "orange"
    yellow = "yellow"
    cyan = "cyan"
    purple = "purple"
    brown = "brown"
    lime = "lime"
    magenta = "magenta"
    gold = "gold"
    black = "black"
    maroon = "maroon"
    darkred = "darkred"
    violet = "violet"
    crimson = "crimson"
    rainbow = "rainbow"


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
        self.start: tuple[int, int] = start
        self.end: tuple[int, int] = end


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
        self.x = x * (50 + 100) + 50
        self.y = y * 100 + (1080 // 2) // 2
        self.color = color
        self.max_drones = max_drones
        self.hub_type = hub_type
        self.zone_type = zone_type
        self.size = 50
        self.surf = pygame.Surface((self.size, self.size))
        self.rect = self.surf.get_rect(center=(self.x, self.y))
        self.text_base = pygame.font.Font("assets/Tiny5.ttf", 20)
        self.text_surf = self.text_base.render(name, True, color)
        self.text_rect = pygame.Rect(
            self.text_surf.get_rect(center=(self.x, self.y + 50))
        )
        self.surf.fill("grey")
        self.to_end = 0


class MapData:
    def __init__(self) -> None:

        self.hubs: dict[str, Hub] = {}
        self.start_hub: Hub | None = None
        self.end_hub: Hub | None = None
        self.connections: list[Connection] = []
        self.drones_number: int = 0
        self.vertical_hubs_number = 0
        self.horizontal_hubs_number = 0
        self.graph: dict[str, list[str]] = {}

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
        self.graph = graph.to_graph(self.connections)


class Drone:

    def __init__(
        self,
        mapdata: MapData,
    ) -> None:
        self.mapdata = mapdata
        self.x = mapdata.start_hub.x
        self.y = mapdata.start_hub.y

        self.size = 30
        self.surf = pygame.Surface((self.size, self.size))
        self.rect = self.surf.get_rect(center=(self.x, self.y))
        self.graph = mapdata.graph
        self.current_hub = mapdata.start_hub.name
        self.surf.fill("red")

    def move(self):
        target_hub: str | None = None

        for hub in self.mapdata.graph[self.current_hub]:
            if target_hub is None:
                target_hub = hub
            elif self.mapdata.hubs[hub].to_end < self.mapdata.hubs[target_hub].to_end:
                target_hub = hub
        self.current_hub = target_hub
        self.x = self.mapdata.hubs[self.current_hub].x
        self.y = self.mapdata.hubs[self.current_hub].y
        self.rect = self.surf.get_rect(center=(self.x, self.y))
