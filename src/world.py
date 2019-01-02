import enum
import pyglet
import logging
import base
from moving import MovingObject, Player, Ghost, Direction

class MapObjects(enum.Enum):
    WALL = "#"
    EMPTY = " "
    PLAYER_SPAWN = "+"
    GHOST_SPAWN = "*"
    GNAMMY_STUFF = "?"
    PLAYER = ":v"
    GHOST = "A"


class PacmanWorld(object):
    """ Representation of the map where pacman and the ghosts live. Needed to planning purposes. """

    class PacmanEntity(object):
        """ """
        def __init__(self, moving_obj, settings):
            self.__settings = settings
            self.entity = moving_obj
            self.row = 0
            self.col = 0
            self.direction = Direction.LEFT

            self.update_coords()

        def update_coords(self):
            """ Update object coordinates in the world matrix and return previous coordinates. """
            row = ((self.__settings.origin_y - self.entity.y) / self.__settings.step)
            col = ((self.entity.x - self.__settings.origin_x) / self.__settings.step)
            rounded_row, rounded_col = round(row), round(col)

            prevs = self.row, self.col

            if abs(row - rounded_row) == 0:
                self.row = rounded_row
            if abs(col - rounded_col) == 0:
                self.col = rounded_col

            return prevs


    def __init__(self):
        """Initialize an empty world"""
        self.__map_size = None
        self.world = None
        self.__pacman = None
        self.__ghosts = None

        self.__settings = base.Settings()

    def _add_wall(x, y):
        base.walls.append(pyglet.sprite.Sprite(img=base.wall.img, x=x, y=y, batch=base.field_batch))


    def __init(self, nrows, ncols):
        """Initialize a nrows*ncols world"""
        self.__map_size = (nrows, ncols)
        #create empty nrows x ncols matrix
        self.world = [[MapObjects.EMPTY] * ncols for _ in range(nrows)]
        self.pacman = None
        self.ghosts = list()

    def update_coords(self, character, dt):
        """Update character's coordinates both in gui and in the matrix.
        Return True if the character moved, False otherwise. """
        entity_type = MapObjects.PLAYER if isinstance(character.entity, Player) else MapObjects.GHOST
        #update position in gui
        character.entity.update(dt)

        #update matrix coordinates
        prev_row, prev_col = character.update_coords()
        #update matrix elements
        if prev_row != character.row or prev_col != character.col:
            self.set_element(MapObjects.EMPTY, prev_row, prev_col)
            self.set_element(entity_type, character.row, character.col)
            return True

        return False

    def update(self, dt):
        """ Update the status of all moving objects """
        self.update_coords(self.pacman, dt)

        for ghost in self.ghosts:
            self.update_coords(ghost, dt)

            #get info about current direction
            c_direction, r_direction, _ = ghost.direction.value

            if self.world[ghost.row+r_direction][ghost.col+c_direction] == MapObjects.WALL:
                print("muro")
                #invert movement direction if there is a wall in front of him
                ghost.entity.direction = Direction.invert_direction(ghost.entity.direction)
                ghost.direction = ghost.entity.direction



    @staticmethod
    def parse_map_file(filename):
        """ Read a file containing a level map and instantiate a PacmanWorld object
        that represent the position and the status of each sprite. """

        logging.basicConfig(level=logging.WARNING)

        world = PacmanWorld()

        try:
            source = pyglet.resource.file(filename, "r")
            line = source.readline().strip()

            if len(line) == 0:
                raise LevelError("Empty file", filename)

            try:
                n_rows, n_cols = [int(x) for x in line.split("x")]
            except ValueError:
                raise LevelError("malformed first line {}".format(line), filename)

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
                    logging.warning("line {} has length {} (expected {})".format(r+1, len(line), n_cols))

                for c, elem in enumerate(line):
#                    print("Init {},{},{}".format(r,c, elem))
                    if c == n_rows:
                        logging.warning("ignoring in excess characters in line {}".format(r))
                        break

                    #get GUI coordinates for current object
                    x_coord = world.__settings.origin_x + world.__settings.step * c
                    y_coord = world.__settings.origin_y - world.__settings.step * r

                    if elem == MapObjects.WALL.value:
                        #add a wall
                        world.set_element(MapObjects.WALL, r, c)
                        PacmanWorld._add_wall(x_coord, y_coord)

                    elif elem == MapObjects.PLAYER_SPAWN.value:
                        #instantiate pacman in the current position
                        pacman = Player()
                        pacman.x, pacman.y = x_coord, y_coord

                        world.set_element(MapObjects.PLAYER, r, c)
                        world.pacman = PacmanWorld.PacmanEntity(pacman, world.__settings)

                        print("PLAYER SPAWN in {}, {}".format(x_coord, y_coord), flush=True)

                    elif elem == MapObjects.GHOST_SPAWN.value:
                        #instantiate a ghost in the current position
                        ghost = Ghost()
                        ghost.x, ghost.y = x_coord, y_coord

                        world.set_element(MapObjects.GHOST, r, c)
                        world.ghosts.append(PacmanWorld.PacmanEntity(ghost, world.__settings))

                        print("GHOST SPAWN in {}, {}".format(x_coord, y_coord), flush=True)

                    elif elem == MapObjects.EMPTY.value:
                        world.set_element(MapObjects.EMPTY, r, c)
                    else:
                        raise LevelError("Unknown symbol: '{}'".format(elem), filename)

        except LevelError as e:
            logging.error(e.default_message())


        return world

    @staticmethod
    def create_borders():
        """ Create a map with walls at all 4 borders (a square)"""
        base.walls = []

        n_blocks_y = base.window.height // base.wall.img.height
        n_blocks_x = base.window.width // base.wall.img.width

        left_border = base.wall.img.anchor_x
        lower_border = base.wall.img.anchor_y
        right_border = base.window.width - base.wall.img.anchor_x
        upper_border = base.window.height - base.wall.img.anchor_y

        for i in range(0, n_blocks_y):
            y = i * base.wall.img.height + base.wall.img.anchor_y
            PacmanWorld._add_wall(x=left_border, y=y)
            PacmanWorld._add_wall(x=right_border, y=y)


        for i in range(0, n_blocks_x):
            x = i * base.wall.img.width + base.wall.img.anchor_x
            PacmanWorld._add_wall(x=x, y=upper_border)
            PacmanWorld._add_wall(x=x, y=lower_border)

    def set_element(self, element_type, row, col):
        self.world[row][col] = element_type


class LevelError(Exception):
    def __init__(self, message, file_name):
        self.message = message
        self.file_name = file_name

    def default_message(self):
        return "message:" + self.message + " for '" + self.file_name + "'"
