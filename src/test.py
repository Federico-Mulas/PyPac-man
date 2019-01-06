from world import PacmanWorld
import planning


if __name__ == "__main__":
    world = PacmanWorld.parse_map_file("level1.txt")
    print(world)

    start = planning.Position(1, 1)
    goal = planning.Position(6, 5)

    print("Start: {}".format(start))
    print("Goal: {}".format(goal))

    plan = planning.a_star_search(start, goal, world)

    for state in plan:
        print("In {}. Apply {}".format(state.position, state.applied))
