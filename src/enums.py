import enum
import pyglet.window.key as key_h

class Actions(enum.Enum):
    "Available movement actions"
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    @property
    def row(self):
        return self.value[0]

    @property
    def col(self):
        return self.value[1]

class Direction(enum.Enum):
    """Represents the possible movements that pacman and ghosts can performself."""
    UP = (0, 1, 270)     # (x movement, y movement, rotation)
    DOWN = (0, -1, 90)
    LEFT = (-1, 0, 180)
    RIGHT = (1, 0, 0)

    @property
    def row(self):
        #magic minus sign fixes all the problemz
        return -self.value[1]

    @property
    def col(self):
        return self.value[0]

    def __repr__(self):
        if self is Direction.UP:
            return "up"
        if self is Direction.DOWN:
            return "down"
        return "left" if self is Direction.LEFT else "right"

    @classmethod
    def get_direction(cls, sprite):
        """Returns the enum value corresponding to the pressed key"""
        if sprite.key_handler[key_h.UP]:
            return cls.UP
        if sprite.key_handler[key_h.LEFT]:
            return cls.LEFT
        if sprite.key_handler[key_h.DOWN]:
            return cls.DOWN
        if sprite.key_handler[key_h.RIGHT]:
            return cls.RIGHT

    @classmethod
    def invert_direction(cls, current_direction):
        if current_direction == cls.LEFT:
            return cls.RIGHT
        if current_direction == cls.RIGHT:
            return cls.LEFT
        if current_direction == cls.UP:
            return cls.DOWN
        if current_direction == cls.DOWN:
            return cls.UP


class MapObjects(enum.Enum):
    WALL = "#"
    EMPTY = " "
    PLAYER_SPAWN = "+"
    GHOST_SPAWN = "*"
    GNAMMY_STUFF = "?"
    PLAYER = ":v"
    GHOST = "A"
