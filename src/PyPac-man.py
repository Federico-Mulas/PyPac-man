#!/usr/bin/env python3
import pyglet
import base
import moving

from world import PacmanWorld


@base.window.event
def on_draw():
    base.window.clear()
    moving.MovingObject.batch.draw()
    base.field_batch.draw()

if __name__ == '__main__':
    #create pacman world and handle user input
    world = PacmanWorld.parse_map_file("level1.txt")
    base.window.push_handlers(world.pacman.entity.key_handler)

#    pyglet.clock.schedule_interval(moving.update, 1/120.0)
    pyglet.clock.schedule_interval(world.update, 1/120.0)
    #level.create_borders() #create full border
    pyglet.app.run()
