from enum import IntEnum


class GrayLevel(IntEnum):
    BLACK = 0
    DARK_GRAY = 255 // 3
    LIGHT_GRAY = 2 * 255 // 3
    WHITE = 255
