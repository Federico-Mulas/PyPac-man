import enum
import world

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


class Position(object):
    def __init__(self, row, col):
        self.__row = row
        self.__col = col

    @property
    def row(self):
        return self.__row

    @property
    def col(self):
        return self.__col

    def apply(self, action):
        """Return the position given by the application of the action to the current position"""
        return Position(self.row + action.row, self.col + action.col)

    def manhattan_distance(self, other):
        return 1#abs(self.__row - other.__row) + abs(self.__col - other.__col)

    def __eq__(self, other):
        return self.__row == other.__row and self.__col == other.__col

    def __str__(self):
        return "({},{})".format(self.row, self.col)

class State(object):
    def __init__(self, position, cost, estimation, action, previous_state = None):
        self.__gcost = cost
        self.__fcost = cost + estimation
        self.__position = position
        self.__prev = previous_state
        self.__action = action

    @property
    def position(self):
        return self.__position

    @property
    def fcost(self):
        return self.__fcost

    @property
    def gcost(self):
        return self.__gcost

    @property
    def previous_state(self):
        return self.__prev

    @property
    def applied(self):
        return self.__action

    def __eq__(self, other):
        return self.position.__eq__(other.position)

    def __str__(self):
        return "{}: f={}, g={}".format(self.position, self.fcost, self.gcost)


class Plan(object):
    def __init__(self, final):
        self.__states = [State(final.position, final.gcost, final.fcost - final.gcost, final.applied)]
        #reconstruct the solution following pointers to the previous state
        prev = final.previous_state
        while prev:
            state = State(prev.position, prev.gcost, prev.fcost - prev.gcost, prev.applied)
            self.__states.insert(0, state)
            prev = prev.previous_state

    @property
    def goal(self):
        return self.__states[-1]

    @property
    def start(self):
        return self.__states[0]

    def __len__(self):
        return len(self.__states)

    def __iter__(self):
        for state in self.__states:
           yield state

#class HighLevelAction(enum.Enum):
#    pass



def validate_position(position, maze):
    """Validate the position in the given world: a position is valid if and only if
    it exists and it is different from a wall (and from a ghost, in the future...)"""
    try:
        worldcell = maze[position.row, position.col]
        validate = position if world.MapObjects.WALL not in worldcell else None
    except IndexError:
        print("boom")
        maxr, maxc = maze.dimension
        row, col = position.row, position.col

        if not 0 <= row < maxr:
            row = 0 if row > 0 else maxr - 1
        if not 0 <= col < maxc:
            col = 0 if row > 0 else maxc - 1

        validate = Position(row, col)
        print(validate)
    return validate


def a_star_search(start, goal, maze):
    #start e goal sono Position
    queue = [State(start, 0, start.manhattan_distance(goal), None)]
    visited = list()

    while len(queue) > 0:
        #pop element with minimum fcost
        current_state = min(queue, key=lambda state: state.fcost)
        queue.remove(current_state)

        if current_state.position == goal:
            return Plan(current_state)

    #        for action, position in get_solution(current_state):
    #            print("Action: {}; position: {}".format(action, position))


    #        raise Exception("E ALLORA IL PIDDIIIIII")

#        print("Current state: {}...".format(current_state), end="")

        if current_state not in visited:
#            print("Expanding...")
            #expand current node
            for action in Actions:
#                print("Applying {}...".format(action), end="")
                #apply action and check the resulting position
                position = validate_position(current_state.position.apply(action), maze)
                if position is not None:
#                    print("Valid")
                    #create new state and add to the queue
                    next_state = State(position, current_state.gcost + 1, position.manhattan_distance(goal), action, current_state)
                    queue.append(next_state)
#                else:
#                    print("Invalid")
            visited.append(current_state)
#        else:
#            print("Already visited")

#    print("fine")
