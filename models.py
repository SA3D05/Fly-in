from enum import Enum


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
