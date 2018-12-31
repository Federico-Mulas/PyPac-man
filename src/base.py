import pyglet

pyglet.resource.path = ['../resources', '../levels']
pyglet.resource.reindex()

window = pyglet.window.Window()
#walls inside the game
class wall:
    img = pyglet.resource.image("block.png")

class pacman:
    img = pyglet.resource.image("pac-man.png")
    spawn_x = window.width / 2
    spawn_y = window.height / 2

class ghost:
    img = pyglet.resource.image("ghost.png")


def set_obj_dimension(dim):
    """ this function set all dimension of objects of the game

        every component will be setted to the same dimension and anchored to it's center

        dim -- dimension to set,
    """
    half_dim = dim/2

    wall.img.height = dim
    wall.img.width = wall.img.height
    wall.img.anchor_x = wall.img.height / 2
    wall.img.anchor_y = wall.img.width / 2

    pacman.img.height = dim - dim/5
    pacman.img.width = pacman.img.height
    pacman.img.anchor_x = pacman.img.height / 2
    pacman.img.anchor_y = pacman.img.height / 2

    ghost.img.height = dim - dim/5
    ghost.img.width = ghost.img.height
    ghost.img.anchor_x = ghost.img.height / 2
    ghost.img.anchor_y = ghost.img.height / 2

#setting default dimension
set_obj_dimension(40)

field_batch = pyglet.graphics.Batch()
ghost_batch = pyglet.graphics.Batch()

walls = []
