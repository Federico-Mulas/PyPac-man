import pyglet
import base
import pyglet.window.key as key_h

import enum

class Direction(enum.Enum):
    """Direction enum represents the possible movements that pacman and ghosts can performself."""
    UP = (None, 1, 270)     # (x movement, y movement, rotation)
    DOWN = (None, -1, 90)
    LEFT = (-1, None, 180)
    RIGHT = (1, None, 0)

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

class MovingObject(pyglet.sprite.Sprite):
    batch = pyglet.graphics.Batch()
    collection = []

    def __init__(self, *args, **kwargs):
        pyglet.sprite.Sprite.__init__(self, batch=MovingObject.batch, *args, **kwargs)
        self.velocity = self.image.width * 7/3
        MovingObject.collection.append(self)

    def collision(self, obj):
        min_x_dist = (self.width + obj.width) / 2
        x_dist = self.x - obj.x
        min_y_dist = (self.height + obj.height) / 2
        y_dist = self.y - obj.y
        return abs(x_dist) < min_x_dist and abs(y_dist) < min_y_dist


    def update(self, move, dt = 0):
        if dt == 0:
            return

        old_coords = self.x, self.y

        if move:
            x_move, y_move, self.rotation = move.value

            if x_move:
                self.x += x_move * self.velocity * dt
            elif y_move:
                self.y += y_move * self.velocity * dt

        for wall in base.walls:
            if self.collision(wall):
                self.x, self.y = old_coords
                break

        self.check_bounds()

    def check_bounds(self):
        min_x = -self.image.width / 2
        min_y = -self.image.height / 2
        max_x = base.window.width + self.image.width / 2
        max_y = base.window.height + self.image.height / 2
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

def update(dt):
    """ very simply but important function that update the status of all moving objects """
    for obj in MovingObject.collection:
        obj.update(dt)
