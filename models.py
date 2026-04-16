from enum import Enum
import pygame


class ZoneType(Enum):
    Normal = "normal"
    Blocked = "blocked"
    Restricted = "restricted"
    Priority = "priority"


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


class HubMetadata:
    def __init__(self) -> None:
        self.zone: ZoneType = ZoneType.Normal
        self.color: Color | None = None
        self.max_drones: int = 1


class ConnectionMetadata:
    def __init__(self) -> None:
        self.max_link_capacity: int = 1


class Hub:
    # hub_w = (WINDOW_W - 2 * margin - (cols - 1) * gap) / cols
    WINDOW_W = 1920
    WINDOW_H = 1080

    cols = 4
    rows = 20

    if cols > rows:
        size = 1080 / (3 * cols + 2)

    else:
        size = 1920 / (3 * rows + 2)
    gap = size * 2
    margin = size * 2

    def __init__(
        self, name: str, size: int, x: int, y: int, metadata: HubMetadata
    ) -> None:
        self.name: str = name
        self.metadata: HubMetadata = metadata
        self.surf = pygame.Surface((self.size, self.size))
        my_x = x * (self.size + self.gap) + self.margin + self.size / 2
        my_y = -y * (self.size + self.gap) + self.WINDOW_H / 2
        self.rect = pygame.Rect(self.surf.get_rect(center=(my_x, my_y)))
        self.text_surf = pygame.font.Font(None, 25).render(name, False, "white")
        self.text_rect = pygame.Rect(
            self.text_surf.get_rect(
                center=(
                    my_x,
                    my_y + (self.size * 0.75),
                )
            )
        )
        pygame.draw.circle(
            self.surf, "red", (self.size / 2, self.size / 2), self.size / 2
        )

        # # for color the hub
        # match metadata.color:
        #     case Color.rainbow:
        #         pygame.draw.circle(self.surf, "white", (100 // 2, 100 // 2), 100 // 2)
        #     case None:
        #         return
        #     case _:
        #         pygame.draw.circle(
        #             self.surf, metadata.color.value, (100 // 2, 100 // 2), 100 // 2
        #         )


class Connection:
    def __init__(
        self, hub_from: str, hub_to: str, metadata: ConnectionMetadata
    ) -> None:
        self.hub_from: str = hub_from
        self.hub_to: str = hub_to
        self.metadata: ConnectionMetadata = metadata


class MapData:
    def __init__(self) -> None:

        self.hubs: dict[str, Hub] = {}
        self.start_hub: Hub | None = None
        self.end_hub: Hub | None = None
        self.connections: list[Connection] = []
        self.drones_number: int = 0

        self.max_x = 0
        self.max_y = 0

    def get_start_hub(self) -> Hub:
        if self.start_hub is None:
            raise ValueError("Start hub cannot be None")
        return self.start_hub

    def get_end_hub(self) -> Hub:
        if self.end_hub is None:
            raise ValueError("End hub cannot be None")
        return self.end_hub
