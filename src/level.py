import pyglet
import base
import logging
import moving
import enum

from world import MapObjects, PacmanWorld

logging.basicConfig(level=logging.WARNING) #filename='example.log'





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
