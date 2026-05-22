"""Enumerations and configuration constants used across the project.

This module defines typed enums for zone and hub types as well as
project-wide configuration values.
"""

from enum import Enum, auto


class ZoneType(Enum):
    """Zone classification affecting routing and access.

    Values:
        RESTRICTED: Higher cost to traverse.
        PRIORITY: Lower cost to traverse.
        BLOCKED: Not traversable.
        NORMAL: Default traversal cost.
    """

    RESTRICTED = auto()
    PRIORITY = auto()
    BLOCKED = auto()
    NORMAL = auto()


class HubType(Enum):
    """Types of hubs present on the map.

    Values:
        START: Starting hub for drones.
        END: Destination hub for drones.
        NORMAL: Regular intermediate hub.
    """

    START = auto()
    END = auto()
    NORMAL = auto()


class Config(Enum):
    """Configuration constants used for display and simulation.

    These values are intentionally stored as an Enum to provide a
    single importable location for constants used throughout the code.
    """

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
    STEP_TIME = 0.2
    CHANGE_COLOR_TIME = 0.3
