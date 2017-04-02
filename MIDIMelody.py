from enum import Enum


class MIDIMelody:
    """Melody which will be generated"""

    class Moods(Enum):
        HAPPY = 1
        SAD = 2
        NOT_SPECIFIED = 3

    class Speeds(Enum):
        SLOW = 80
        MEDIUM = 108
        FAST = 120
