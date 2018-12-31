import pyglet
import base
import logging
import moving
logging.basicConfig(level=logging.WARNING) #filename='example.log'

import enum

class MapObjects(enum.Enum):
    WALL = "#"
    EMPTY = " "
    PLAYER_SPAWN = "+"
    GHOST_SPAWN = "*"
    GNAMMY_STUFF = "?"

# WALL_CHAR  = '#'
# BLANK_CHAR = ' '
# SPAWN_CHAR = '+'

def add_wall(x, y):
    base.walls.append(pyglet.sprite.Sprite(img=base.wall.img, x=x, y=y, batch=base.field_batch))

def add_ghost(ghost):
    base.ghosts.append(pyglet.sprite.Sprite(img=base.ghost.img, x=ghost.x, y=ghost.y, batch=moving.MovingObject.batch))

def create_borders():
    """ Create walls i all 4 borders """
    base.walls = []

    n_blocks_y = base.window.height // base.wall.img.height
    n_blocks_x = base.window.width // base.wall.img.width

    left_border = base.wall.img.anchor_x
    lower_border = base.wall.img.anchor_y
    right_border = base.window.width - base.wall.img.anchor_x
    upper_border = base.window.height - base.wall.img.anchor_y
    for i in range(0, n_blocks_y):
        y = i * base.wall.img.height + base.wall.img.anchor_y
        add_wall(x=left_border, y=y)
        add_wall(x=right_border, y=y)


    for i in range(0, n_blocks_x):
        x = i * base.wall.img.width + base.wall.img.anchor_x
        add_wall(x=x, y=upper_border)
        add_wall(x=x, y=lower_border)


class LevelError(Exception):
    def __init__(self, message, file_name):
        self.message = message
        self.file_name = file_name

    def default_message(self):
        return "message:" + self.message + " for '" + self.file_name + "'"


def create_from_file(file_name, player):
    base.walls = []

    try:
        source = pyglet.resource.file(file_name, "r")
        #get header
        line = source.readline()

        if line == "":
            raise LevelError("empty file", file_name)

        rc = line.strip().split("x")
        if len(rc) != 2:
            raise LevelError("malformed first line " + line, file_name)

        n_rows, n_cols = [int(x) for x in rc]

        #calculating step to obtain nicely placed square walls
        step = min(base.window.height // n_rows, base.window.width // n_cols)

        #resizing blocks and packman
        base.set_obj_dimension(step)

        #resizing window to fit
        base.window.height = step * n_rows
        base.window.width  = step * n_cols

        # Using upper left border to as origin
        origin_x = step / 2
        origin_y = base.window.height - step / 2

        for r, line in enumerate(source):
            line = line.strip()

            if len(line) != n_cols:
                pass #che fare?

            for c, elem in enumerate(line):
                if c == n_rows:
                    pass #wtf

                if elem == MapObjects.WALL.value:
                    add_wall(x = origin_x + step * c, y = origin_y - step * r)
                elif elem == MapObjects.PLAYER_SPAWN.value:
                    player.x = origin_x + step * c
                    player.y = origin_y - step * r
                    player.update()
                elif elem == MapObjects.GHOST_SPAWN.value:
                    ghost = moving.Ghost()
                    ghost.x = origin_x + step * c
                    ghost.y = origin_y - step * r
                elif elem == MapObjects.EMPTY.value:
                    pass
                else:
                    raise LevelError("Unknown char: '{}'".format(elem), file_name)

    except LevelError as e:
        logging.error(e.default_message())
