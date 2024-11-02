from enum import StrEnum, auto

class Anchor(StrEnum):
    MOUSE = auto()

    CENTER = auto()

    TOP = auto()
    TOP_MIDDLE = auto()
    TOP_LEFT = auto()
    TOP_RIGHT = auto()

    LEFT = auto()
    LEFT_MIDDLE = auto()

    RIGHT = auto()
    RIGHT_MIDDLE = auto()

    BOTTOM = auto()
    BOTTOM_MIDDLE = auto()
    BOTTOM_LEFT = auto()
    BOTTOM_RIGHT = auto()
