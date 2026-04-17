from enum import Enum
from pprint import pprint
import pygame


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


# class ConnectionMetadata:
#     def __init__(self) -> None:
#         self.max_link_capacity: int = 1


class Hub:

    screen_w = 0
    screen_h = 0

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

        self.name: str = name
        self.x = x
        self.y = y
        self.color = color
        self.max_drones = max_drones
        self.hub_type = hub_type
        self.zone_type = zone_type

        my_x = x * (100 + 400) + 100
        my_y = y * 200 + 1080 / 2

        Hub.screen_w = max(Hub.screen_w, my_x)
        Hub.screen_h = max(Hub.screen_h, my_y)

        self.surf = pygame.Surface((100, 100))
        self.rect = self.surf.get_rect(
            center=(
                my_x,
                my_y,
            )
        )

        self.text_base = pygame.font.Font("assets/Anto.ttf", 20)
        self.text_surf = self.text_base.render(name, True, color)
        self.text_rect = pygame.Rect(
            self.text_surf.get_rect(
                center=(
                    my_x,
                    my_y + 100,
                )
            )
        )
        self.surf.fill("grey")


class MapData:
    def __init__(self) -> None:

        self.hubs: dict[str, Hub] = {}
        self.start_hub: Hub | None = None
        self.end_hub: Hub | None = None
        # self.connections: list[Connection] = []
        self.drones_number: int = 0
        self.vertical_hubs_number = 0
        self.horizontal_hubs_number = 0

    def get_start_hub(self) -> Hub:
        if self.start_hub is None:
            raise ValueError("Start hub cannot be None")
        return self.start_hub

    def get_end_hub(self) -> Hub:
        if self.end_hub is None:
            raise ValueError("End hub cannot be None")
        return self.end_hub

    def build_obj(self, raw_data: dict) -> tuple:
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
            self.vertical_hubs_number = max(
                self.vertical_hubs_number, abs(hub["y"]) + 1
            )
            self.horizontal_hubs_number = max(self.horizontal_hubs_number, hub["x"] + 1)
        return (Hub.screen_w, Hub.screen_h)
