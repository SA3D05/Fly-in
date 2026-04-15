from enum import Enum
from pygame import SRCALPHA, Surface, font, Rect, draw


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
    def __init__(self, name: str, x: int, y: int, metadata: HubMetadata) -> None:
        self.x: int = x
        self.y: int = y
        self.name: str = name
        self.metadata: HubMetadata = metadata
        self.surface = Surface((100, 100), SRCALPHA)
        draw.circle(self.surface, (255, 0, 0), (100 // 2, 100 // 2), 100 // 2)
        self.rect = Rect(
            self.surface.get_rect(
                center=(
                    (
                        x * 100,
                        y * 100,
                    ),
                )
            )
        )
        self.text = font.Font(None, 25).render(name, False, "white")
        self.recttext = Rect(self.text.get_rect(center=(0, 0)))

        # match metadata.color:
        #     case Color.rainbow:
        #         self.surface.fill(metadata.color.value)
        #     case None:
        #         return
        #     case _:
        #         self.surface.fill(metadata.color.value)


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

    def get_start_hub(self) -> Hub:
        if self.start_hub is None:
            raise ValueError("Start hub cannot be None")
        return self.start_hub

    def get_end_hub(self) -> Hub:
        if self.end_hub is None:
            raise ValueError("End hub cannot be None")
        return self.end_hub
