from enum import Enum


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
