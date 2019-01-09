import enum
import logging
import pyglet
import random

import base
import moving
import entity
from enums import Direction, MapObjects


class WorldCell(object):
    """ Representation of a cell matrix. Multiple objects can live simultaneously in the same cell """

    def __init__(self, row, col, content=MapObjects.EMPTY):
        #cell coordinates (a little bit redundant, but maybe they will be useful)
        self.__coords = (row, col)
        #what objects are present in the cell
        self.__content = [content]
        #which entities are present in the cell
        self.__entity = list()

    @property
    def row(self):
        return self.__coords[0]

    @property
    def col(self):
        return self.__coords[1]

    def add(self, entity):
        """Add an entity in the cell"""
        self.__content.append(entity.type)
        self.__entity.append(entity)

    def remove(self, entity):
        """Remove the given entity from the cell"""
        if entity in self.__entity: #because life sucks
            self.__content.remove(entity.type)
            self.__entity.remove(entity)

    def __contains__(self, item):
        """Check the presence of a certain item (a MapObjects instance) in the cell"""
        return item in self.__content

    def __repr__(self):
        return "".join([v.value for v in self.__content])




class PacmanWorld(object):
    """ Representation of the map where pacman and the ghosts live. Needed to planning purposes. """

    def __init__(self):
        """Initialize an empty world"""
        self.__map_size = None
        self.world = None
        self.__pacman = None
        self.__ghosts = None

        self.__settings = base.Settings()


    def __init(self, nrows, ncols):
        """Initialize a nrows*ncols world"""
        self.__map_size = (nrows, ncols)
        #create empty nrows x ncols matrix
        self.world = [
            [WorldCell(nr, nc) for nc in range(ncols)]
            for nr in range(nrows)
        ]

        self.pacman = None
        self.ghosts = list()

    @property
    def dimension(self):
        return self.__map_size

    def __getitem__(self, key):
        """Get the element in the [row, col] cell"""
        row, col = key
        return self.world[row][col]

    def __setitem__(self, key, item):
        """Set the content of the [row,col] cell"""
        row, col = key
        self.world[row][col].add(item)

    def set_element(self, element_type, row, col):
        """Set the content of the [row,col] cell. It supports ONLY fixed objects"""
        self.world[row][col] = WorldCell(row, col, element_type)

    def update_coords(self, character, dt):
        """Update character's coordinates both in gui and in the matrix.
        Return True if the character has been moved, False otherwise. """
        #update position in gui
        character.entity.update(dt)
        #update matrix coordinates
        prev_row, prev_col = character.update_coords()
        #check if coordinates has been updated
        update = prev_row != character.row or prev_col != character.col
        #update matrix elements
        if update:
            self[prev_row, prev_col].remove(character)
            self[character.row, character.col].add(character)
            logging.info("{} moving from ({},{}) to ({},{})".format(character.type, prev_row, prev_col, character.row, character.col))

        return update

    def update(self, dt):
        """ Update the status of all moving objects """

        #update ghosts
        for ghost in self.ghosts:
            if self.update_coords(ghost, dt):
                ghost.next_move(self)
        else:
            #then update pacman
            self.update_coords(self.pacman, dt)


    def __str__(self):
        """Print the current state of the world"""
        return str("\n".join([str(row) for row in self.world]))

    @staticmethod
    def parse_map_file(filename):
        """ Read a file containing a level map and instantiate a PacmanWorld object
        that represent the position and the status of each sprite. """

        logging.getLogger().setLevel(logging.WARNING)
        world = PacmanWorld()

        with pyglet.resource.file(filename, "r") as source:
            try:
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
                # Using upper left border as origin
                world.__settings.origin_x = world.__settings.step / 2
                world.__settings.origin_y = base.window.height - world.__settings.step / 2

                world.__init(n_rows, n_cols)
                ghost_list = list()

                for r, line in enumerate(source):
                    line = line.strip()

                    if len(line) != n_cols:
                        logging.warning("line {} has length {} (expected {})".format(r+1, len(line), n_cols))

                    for c, elem in enumerate(line):
                        if c == n_rows:
                            logging.warning("ignoring in excess characters in line {}".format(r))
                            break

                        #get GUI coordinates for current object
                        x_coord = world.__settings.origin_x + world.__settings.step * c
                        y_coord = world.__settings.origin_y - world.__settings.step * r

                        if elem == MapObjects.WALL.value:
                            #add a wall both in matrix and GUI
                            world.set_element(MapObjects.WALL, r, c)
                            PacmanWorld.__add_wall(x_coord, y_coord)

                        elif elem == MapObjects.PLAYER_SPAWN.value:
                            #instantiate pacman in the current position
                            pacman = moving.Player().set_coordinates(x_coord, y_coord)
                            #set spawning point in the map
                            world.set_element(MapObjects.PLAYER_SPAWN, r, c)
                            world.pacman = entity.Pacman(pacman, world.__settings).set_spawn(r, c)

                            logging.info("PLAYER SPAWN in {}, {}".format(x_coord, y_coord))

                        elif elem == MapObjects.GHOST_SPAWN.value:
                            #instantiate a ghost in the current position
                            ghost = moving.Ghost().set_coordinates(x_coord, y_coord)
                            ghost_list.append(entity.Ghost(ghost, world.__settings).set_spawn(r, c))
                            #set spawning point in the map
                            world.set_element(MapObjects.GHOST_SPAWN, r, c)

                            logging.info("GHOST SPAWN in {}, {}".format(x_coord, y_coord))

                        elif elem != MapObjects.EMPTY.value:
                            raise LevelError("Unknown symbol: '{}'".format(elem), filename)

            except LevelError as e:
                logging.error(e.default_message())

        #initialize ghosts' direction based on available ones
        for ghost in ghost_list:
            ghost.direction = random.choice(ghost.available_directions(world))
            world.ghosts.append(ghost)

        return world

    @staticmethod
    def create_borders():
        """ Create a map with walls at all 4 borders (a square)"""
        base.walls = list()

        n_blocks_y = base.window.height // base.wall.img.height
        n_blocks_x = base.window.width // base.wall.img.width

        left_border = base.wall.img.anchor_x
        lower_border = base.wall.img.anchor_y
        right_border = base.window.width - base.wall.img.anchor_x
        upper_border = base.window.height - base.wall.img.anchor_y

        for i in range(n_blocks_y):
            y = i * base.wall.img.height + base.wall.img.anchor_y
            PacmanWorld.__add_wall(x=left_border, y=y)
            PacmanWorld.__add_wall(x=right_border, y=y)


        for i in range(n_blocks_x):
            x = i * base.wall.img.width + base.wall.img.anchor_x
            PacmanWorld.__add_wall(x=x, y=upper_border)
            PacmanWorld.__add_wall(x=x, y=lower_border)


    def __add_wall(x, y):
        base.walls.append(pyglet.sprite.Sprite(img=base.wall.img, x=x, y=y, batch=base.field_batch))


class LevelError(Exception):
    def __init__(self, message, file_name):
        self.message = message
        self.file_name = file_name

    def default_message(self):
        return "message:" + self.message + " for '" + self.file_name + "'"
