import pyglet
import base
import logging
import moving
logging.basicConfig(level=logging.WARNING) #filename='example.log'

WALL_CHAR  = '#'
BLANK_CHAR = ' '
SPAWN_CHAR = '+'

def add_wall(x, y):
    base.walls.append(pyglet.sprite.Sprite(img=base.wall.img, x=x, y=y, batch=base.field_batch))

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
        with open(file_name, 'r') as source:
            line = source.readline()
            if line == "":
                raise LevelError("empty file", file_name)

            rc = line.rstrip().split("x")
            if len(rc) != 2:
                raise LevelError("malformed first line " + line, file_name)

            n_rows = int(rc[0])
            n_cols = int(rc[1])

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

            line = source.readline()
            r = 0
            while line != "" and n_rows > r:
                c = 0
                for elem in line:
                    if   WALL_CHAR  == elem:
                        add_wall(x = origin_x + step * c , y = origin_y - step * r)
                    elif BLANK_CHAR == elem:
                        pass #nothing to do
                    elif SPAWN_CHAR == elem:
                        player.x = origin_x + step * c
                        player.y = origin_y - step * r
                        player.update()
                    else:
                        raise LevelError("unknown char : '" + elem + "'", file_name)
                    c += 1
                    if c == n_cols:
                        break
                r += 1
                line = source.readline()

    except LevelError as e:
        logging.error(e.default_message())

