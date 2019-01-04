import pyglet
import base
import pyglet.window.key as key_h

import enum

class Direction(enum.Enum):
    """Direction enum represents the possible movements that pacman and ghosts can performself."""
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

class MovingObject(pyglet.sprite.Sprite):
    batch = pyglet.graphics.Batch()
    collection = []

    def __init__(self, *args, **kwargs):
        pyglet.sprite.Sprite.__init__(self, batch=MovingObject.batch, *args, **kwargs)
        MovingObject.collection.append(self)

        self.velocity = self.image.width * 7/3
        self.last_move = None
        self.direction = None

    def set_coordinates(self, x, y):
        self.x, self.y = x, y
        return self

    def collision(self, obj):
        min_x_dist = (self.width + obj.width) / 2
        x_dist = self.x - obj.x
        min_y_dist = (self.height + obj.height) / 2
        y_dist = self.y - obj.y
        return abs(x_dist) < min_x_dist and abs(y_dist) < min_y_dist


    def update(self, move, dt = 0):
        if dt == 0:
            return

        _x, _y = self.x, self.y
        last_move = self.last_move

        if move:
            x_direction, y_direction, self.rotation = move.value

            self.x += int(x_direction * self.velocity * dt)
            self.y += int(y_direction * self.velocity * dt)
            self.last_move = move

        for wall in base.walls:
            if self.collision(wall):
                self.set_coordinates(_x, _y)
                self.last_move = last_move
                break

        self.check_bounds()

    def check_bounds(self):
        min_x, min_y = -self.image.width // 2, -self.image.height // 2
        max_x, max_y = base.window.width - min_x, base.window.height - min_y

        if self.x < min_x:
            self.x = max_x
        elif self.x > max_x:
            self.x = min_x
        if self.y < min_y:
            self.y = max_y
        elif self.y > max_y:
            self.y = min_y

class Player(MovingObject):
    def __init__(self, *args, **kwargs):
        MovingObject.__init__(self, img=base.pacman.img, *args, **kwargs)
        self.key_handler = key_h.KeyStateHandler()

    def update(self, dt = 0):
        movement = Direction.get_direction(self)
        super().update(movement, dt)



class Ghost(MovingObject):
    def __init__(self, *args, **kwargs):
        MovingObject.__init__(self, img=base.ghost.img, *args, **kwargs)

    def update(self, dt = 0):
        super().update(self.direction, dt)
