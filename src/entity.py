from abc import ABC, abstractmethod
import logging
import random

from enums import MapObjects, Direction
import moving
#from moving import MovingObject, Player, Ghost

class AbstractEntity(ABC):
    def __init__(self, moving_obj, settings):
        """Representation of a moving entity living in the world"""
        self.__settings = settings
        self.__row = None
        self.__col = None
        self.__spawn = None
        self.__direction = moving_obj.direction
        self.entity = moving_obj
        self.__type = MapObjects.GHOST if isinstance(moving_obj, moving.Ghost) else MapObjects.PLAYER

        self.update_coords()

    #getters and setters
    @property
    def row(self):
        return self.__row

    @property
    def col(self):
        return self.__col

    @property
    def direction(self):
        return self.__direction

    @property
    def type(self):
        return self.__type

    @direction.setter
    def direction(self, value):
        self.__direction = self.entity.direction = value

    def set_spawn(self, row, col):
        self.__spawn = row, col
        return self

    def distance(self, other, action):
        """Compute Manhattan distance between 'self' and 'other', considering
        that 'self' will perform the selected action"""
        return abs(other.row - self.row - action.row) + abs(other.col - self.col - action.col)

    def update_coords(self):
        """ Update object coordinates (locally in the object) and return previous coordinates. """
        #calculate matrix cell based on GUI coordinates
        row = ((self.__settings.origin_y - self.entity.y) / self.__settings.step)
        col = ((self.entity.x - self.__settings.origin_x) / self.__settings.step)
        rounded_row, rounded_col = round(row), round(col)
        #store current coordinates
        prevs = self.__row, self.__col

        #update coordinates, if they are changed
        if abs(row - rounded_row) == 0:
            self.__row = rounded_row
        if abs(col - rounded_col) == 0:
            self.__col = rounded_col

        return prevs


    def available_directions(self, worldmap):
        #check possible direction from current position. An IndexError is raised
        #if pacman-effect verifies (what does it mean? I don't know)
        try:
            available = [
                current for current in Direction
                if MapObjects.WALL not in worldmap[self.row+current.row, self.col+current.col]
            ]
        except IndexError:
            #go head! (inverse direction is present for compatibility reason)
            available = [self.direction, Direction.invert_direction(self.direction)]
        finally:
            logging.info("Position during planning: {},{}: found: {}".format(self.row, self.col, available))

        return available

    @abstractmethod
    def next_move(self, world):
        pass

class Pacman(AbstractEntity):
    def __init__(self, moving_obj, settings):
        super().__init__(moving_obj, settings)

    def next_move(self, world):
        print("Unsupported")

class Ghost(AbstractEntity):
    def __init__(self, moving_obj, settings):
        super().__init__(moving_obj, settings)

    def next_move(self, world):
        #get available directions
        actions = super().available_directions(world)
        #remove the inverse direction from the available ones (it is present for sure)
        #it will be selected if and only if no other directions are available
        chosen_direction = Direction.invert_direction(self.entity.direction)
        actions.remove(chosen_direction)
        #find best direction from available ones
        if len(actions) > 0:
            #calculate costs and find the minimum one
            costs = [(action, super(Ghost, self).distance(world.pacman, action)) for action in actions]
            min_cost = min(costs, key=lambda pair: pair[1])[1]
            #get random action with minimum cost
            chosen_direction = random.choice([action for action, cost in costs if cost == min_cost])

        self.entity.direction = self.direction = chosen_direction
        logging.info("planning in {},{}. available: {}, decision: {}".format(self.row, self.col, actions, chosen_direction))
