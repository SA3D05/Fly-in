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
    FONT_PATH = "assets/font.ttf"
    INFO_TEXT_SIZE = 80
    CONNECTION_COLOR = "white"
    CONNECTION_SIZE = 2
    HUB_SIZE = 60
    HUB_TEXT_SIZE = 30
    BORDERS_COLOR = "white"
    HUB_SPRITE = "assets/hub.png"
    DRONE_SPRITE = "assets/drone.png"
    BACKGROUND_COLOR = (32, 32, 32)
    PRIME_COLOR = "white"
    MAP_FILE = "maps/challenger/01_the_impossible_dream.txt"
    STEP_TIME = 0
    CHANGE_COLOR_TIME = 0.3
