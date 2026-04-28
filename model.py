from globals import DRONE_IMG, DRONE_SIZE, FONT_FAMILY_PATH, HUB_NAME_SIZE, HUB_SIZE
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

        self.text_base = pygame.font.Font(FONT_FAMILY_PATH, HUB_NAME_SIZE)
        self.text_surf = self.text_base.render(f"{name}", True, "white", "black")

        self.to_end = 0
        self.drones_setting = 0

    def get_coordinates(self) -> tuple[int, int]:
        return (self.x, self.y)


class MapData:
    def __init__(self) -> None:

        self.hubs: dict[str, Hub] = {}
        self.connections: list[Connection] = []

        self.start_hub: Hub | None = None
        self.end_hub: Hub | None = None
        self.drones_number: int = 0
        self.vertical_hubs_number: int = 1
        self.horizontal_hubs_number: int = 1

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
            self.vertical_hubs_number = max(self.vertical_hubs_number, hub["y"] + 1)
            self.horizontal_hubs_number = max(self.horizontal_hubs_number, hub["x"] + 1)

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

    def __init__(self, id: int, coordinates: tuple[int, int]) -> None:

        self.id = id
        self.x, self.y = coordinates
        self.path_idx: int = 0

        img = pygame.image.load(DRONE_IMG)
        img = pygame.transform.rotate(img, -90)
        self.surf = pygame.transform.smoothscale(img, (DRONE_SIZE, DRONE_SIZE))

        self.text_base = pygame.font.Font(FONT_FAMILY_PATH, DRONE_SIZE)
        # self.surf = self.text_base.render(
        #     f"{id}",
        #     True,
        #     "white",
        # )

        self.reach_goal: bool = False

    def get_coordinates(self) -> tuple[int, int]:
        return (self.x, self.y)
