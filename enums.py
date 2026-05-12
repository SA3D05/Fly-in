from enum import Enum, auto


class ZoneType(Enum):
    RESTRICTED = auto()
    PRIORITY = auto()
    BLOCKED = auto()
    NORMAL = auto()


class HubType(Enum):
    START = auto()
    END = auto()
    NORMAL = auto()


class Config(Enum):
    FONT_PATH = "assets/Tiny5.ttf"
    INFO_TEXT_SIZE = 80
    CONNECTION_COLOR = "grey"
    CONNECTION_SIZE = 2
    HUB_SIZE = 60
    HUB_TEXT_SIZE = 30

    HUB_SPRITE = "assets/hub.png"
    DRONE_SPRITE = "assets/drone.png"

    MAP_FILE = "maps/challenger/01_the_impossible_dream.txt"
    DRONES_SPEED = 5
