import enum
import pyglet

import base
import level
from moving import MovingObject, Player, Ghost


class MapObjects(enum.Enum):
    WALL = "#"
    EMPTY = " "
    PLAYER_SPAWN = "+"
    GHOST_SPAWN = "*"
    GNAMMY_STUFF = "?"
    PLAYER = "bah" #
    GHOST = "boh"


class PacmanWorld(object):
    """ Representation of the map where pacman and the ghosts live. Needed to planning purposes. """

    class PacmanEntity(object):
        """ """
        def __init__(self, moving_obj, settings):
            self.__settings = settings
            self.entity = moving_obj
            self.x = 0
            self.y = 0

            self.update_coords()

        def update_coords(self):
            """ Return object coordinates in the world matrix.  """
            self.x = round((self.__settings.origin_y - self.entity.y) / self.__settings.step)
            self.y = round((self.entity.x - self.__settings.origin_x) / self.__settings.step)


    def __init__(self):
        self.__map_size = None
        self.world = None
        self.__pacman = None
        self.__ghosts = None

        self.__settings = base.Settings()



    def __init(self, nrows, ncols):
        self.__map_size = (nrows, ncols)
        #create empty nrows x ncols matrix
        self.world = [[MapObjects.EMPTY] * ncols for _ in range(nrows)]
        self.pacman = None
        self.ghosts = list()



    def update(self, dt):
        """ very simply but important function that update the status of all moving objects """
        self.pacman.entity.update(dt)
        self.pacman.update_coords()
#        print("Pacman in ({},{})".format(self.pacman.x, self.pacman.y))

        for ghost in self.ghosts:
            ghost.entity.update(dt)
            ghost.update_coords()
#            print("Ghost in ({}, {})".format(ghost.x, ghost.y))



    @staticmethod
    def parse_map_file(filename):
        """ Read a file containing a level map and instantiate a PacmanWorld object
        that represent the position and the status of each sprite. """

        world = PacmanWorld()

        try:
            source = pyglet.resource.file(filename, "r")
            line = source.readline().strip()

            if len(line) == 0:
                raise LevelError("Empty file", filename)

            n_rows, n_cols = [int(x) for x in line.split("x")]

            #calculating step to obtain nicely placed square walls
            world.__settings.step = min(base.window.height // n_rows, base.window.width // n_cols)

            #resizing blocks and packman
            base.set_obj_dimension(world.__settings.step)

            #resizing window to fit
            base.window.height = world.__settings.step * n_rows
            base.window.width  = world.__settings.step * n_cols

            # Using upper left border to as origin
            world.__settings.origin_x = world.__settings.step / 2
            world.__settings.origin_y = base.window.height - world.__settings.step / 2

            print(world.__settings.origin_x, world.__settings.origin_y, world.__settings.step)

            world.__init(n_rows, n_cols)

            for r, line in enumerate(source):
                line = line.strip()

                if len(line) != n_cols:
                    pass    #TODO

                for c, elem in enumerate(line):
                    if c == n_rows:
                        pass #TODO

                    #get GUI coordinates for current object
                    x_coord = world.__settings.origin_x + world.__settings.step * c
                    y_coord = world.__settings.origin_y - world.__settings.step * r

                    if elem == MapObjects.WALL.value:
                        world.set_element(MapObjects.WALL, r, c)
                        level.add_wall(x_coord, y_coord)

                    elif elem == MapObjects.PLAYER_SPAWN.value:
                        pacman = Player()
                        pacman.x, pacman.y = x_coord, y_coord

                        world.set_element(MapObjects.PLAYER, r, c)
                        world.pacman = PacmanWorld.PacmanEntity(pacman, world.__settings)

                        print("PLAYER SPAWN in {}, {}".format(x_coord, y_coord), flush=True)

                    elif elem == MapObjects.GHOST_SPAWN.value:
                        ghost = Ghost()
                        ghost.x, ghost.y = x_coord, y_coord

                        world.set_element(MapObjects.GHOST, r, c)
                        world.ghosts.append(PacmanWorld.PacmanEntity(ghost, world.__settings))

                        print("GHOST SPAWN in {}, {}".format(x_coord, y_coord), flush=True)

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
