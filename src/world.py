import enum
import pyglet

import base
import level
from moving import Player, Ghost


class MapObjects(enum.Enum):
    WALL = "#"
    EMPTY = " "
    PLAYER_SPAWN = "+"
    GHOST_SPAWN = "*"
    GNAMMY_STUFF = "?"
    PLAYER = "bah" #
    GHOST = "boh"

class PacmanWorld(object):
    def __init__(self, nrows, ncols):
        #create empty nrows x ncols matrix
        self.world = [[MapObjects.EMPTY] * ncols for _ in range(nrows)]
        self.pacman = None
        self.ghosts = list()

    @staticmethod
    def parse_map_file(filename):
        world = None

        try:
            source = pyglet.resource.file(filename, "r")
            line = source.readline().strip()

            if len(line) == 0:
                raise LevelError("Empty file", filename)

            n_rows, n_cols = [int(x) for x in line.split("x")]

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

            world = PacmanWorld(n_rows, n_cols)

            for r, line in enumerate(source):
                line = line.strip()

                if len(line) != n_cols:
                    pass #TODO

                for c, elem in enumerate(line):
                    if c == n_rows:
                        pass #TODO

                    x_coord = origin_x + step * c
                    y_coord = origin_y - step * r

                    if elem == MapObjects.WALL.value:
                        world.set_element(MapObjects.WALL, r, c)
                        level.add_wall(x_coord, y_coord)

                    elif elem == MapObjects.PLAYER_SPAWN.value:
                        world.pacman = Player()
                        world.pacman.x = x_coord
                        world.pacman.y = y_coord
                        world.set_element(MapObjects.PLAYER, r, c)

                    elif elem == MapObjects.GHOST_SPAWN.value:
                        ghost = Ghost()
                        ghost.x = x_coord
                        ghost.y = y_coord

                        world.set_element(MapObjects.GHOST, r, c)
                        world.ghosts.append(ghost)

                    elif elem == MapObjects.EMPTY.value:
                        world.set_element(MapObjects.EMPTY, r, c)
                    else:
                        raise LevelError("Unknown symbol: '{}'".format(elem), file_name)

        except ValueError as e:
            #failed to split first line of the file 
            logging.error(e)
        except LevelError as e:
            logging.error(e.default_message())

        return world

    def set_element(self, element_type, x, y, obj = None):
        self.world[x][y] = element_type


class LevelError(Exception):
    def __init__(self, message, file_name):
        self.message = message
        self.file_name = file_name

    def default_message(self):
        return "message:" + self.message + " for '" + self.file_name + "'"
