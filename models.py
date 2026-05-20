from pprint import pprint

from enums import Config, HubType, ZoneType
import pygame


class Hub:

    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        color: str,
        max_drones: int,
        hub_type: HubType,
        zone_type: ZoneType,
    ) -> None:

        self.name: str = name
        self.x: int = x
        self.y: int = y
        self.color: str = color
        self.max_drones: int = int(max_drones)
        self.hub_type: HubType = hub_type
        self.zone_type: ZoneType = zone_type

        self.surf: None | pygame.surface.Surface = None
        self.text_base: pygame.Font = pygame.font.Font(
            Config.FONT_PATH.value, Config.HUB_TEXT_SIZE.value
        )
        self.text_surf: pygame.surface.Surface = self.text_base.render(
            f"{name}", True, "white"
        )

        self.to_end: int = 0
        self.drones_setting: int = 0

    def is_restricted(self) -> bool:
        if self.zone_type == ZoneType.RESTRICTED:
            return True
        return False

    def get_coordinates(self) -> tuple[int, int]:
        return (self.x, self.y)

    def can_enter(self) -> bool:
        if self.hub_type == HubType.END:
            return True
        if self.drones_setting < self.max_drones:
            return True
        return False


class Connection:

    def __init__(
        self,
        hub_from: Hub,
        hub_to: Hub,
        start_coordinates: tuple[int, int],
        end_coordinates: tuple[int, int],
        max_link_capacity: int = 1,
    ) -> None:

        self.hub_from: Hub = hub_from
        self.hub_to: Hub = hub_to
        self.max_link_capacity: int = max_link_capacity
        self.start_coordinates: tuple[int, int] = start_coordinates
        self.end_coordinates: tuple[int, int] = end_coordinates
        self.drones_passing: int = 0

    def can_pass(self) -> bool:
        if self.drones_passing < self.max_link_capacity:
            return True

        return False


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
        self.drones_number = raw_data["nb_drones"]
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
            if hub["type"] == HubType.START:
                self.start_hub = self.hubs[hub["name"]]
            elif hub["type"] == HubType.END:
                self.end_hub = self.hubs[hub["name"]]

        for c in raw_data["connections"]:

            hub_from: Hub = self.hubs[c["hub_from"]]
            hub_to: Hub = self.hubs[c["hub_to"]]
            max_link_capacity: int = c["max_link_capacity"]

            self.connections.append(
                Connection(
                    hub_from,
                    hub_to,
                    hub_from.get_coordinates(),
                    hub_to.get_coordinates(),
                    max_link_capacity,
                )
            )

        self.graph: dict = {}


class Drone:

    def __init__(
        self,
        id: int,
        current_hub: Hub,
        x: float,
        y: float,
        current_connection: Connection,
    ) -> None:

        self.id = id
        self.x: float = x
        self.y: float = y

        self.current_hub: Hub = current_hub

        img = pygame.image.load(Config.DRONE_SPRITE.value)
        self.surf = pygame.transform.smoothscale(img, (100, 100))

        self.text_base = pygame.font.Font(Config.FONT_PATH.value, 50)
        self.text_surf = self.text_base.render(f"{id}", True, "white")
        self.reach_goal: bool = False
        self.in_connection: bool = False
        self.current_connection: Connection = current_connection

    def get_coordinates(self) -> tuple[float, float]:
        return (self.x, self.y)
