import pyglet
import base
import level
import moving


#create pacman and handle user input
pacman = moving.Player()
base.window.push_handlers(pacman.key_handler)

@base.window.event
def on_draw():
    base.window.clear()
    moving.MovingObject.batch.draw()
    base.field_batch.draw()

if __name__ == '__main__':
    level.create_from_file("./levels/level1.txt", pacman)
    pyglet.clock.schedule_interval(moving.update, 1/120.0)
    #level.create_borders() #create full border
    pyglet.app.run()
