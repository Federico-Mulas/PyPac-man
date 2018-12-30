import pyglet
import moving
import base

#create pacman and handle user input
pacman = moving.Player(x=base.window.width / 2, y=base.window.height / 2)
base.window.push_handlers(pacman.key_handler)

def create_borders():
    """ Create walls i all 4 borders """
    # TODO load walls structure from file

    n_blocks_y = base.window.height // base.wall_img.height
    n_blocks_x = base.window.width // base.wall_img.width

    left_border = base.wall_img.anchor_x
    lower_border = base.wall_img.anchor_y
    right_border = base.window.width - base.wall_img.anchor_x
    upper_border = base.window.height - base.wall_img.anchor_y
    for i in range(0, n_blocks_y):
        y = i * base.wall_img.height + base.wall_img.anchor_y
        base.walls.append(pyglet.sprite.Sprite(img=base.wall_img, x=left_border, y=y, batch=base.field_batch))
        base.walls.append(pyglet.sprite.Sprite(img=base.wall_img, x=right_border, y=y, batch=base.field_batch))


    for i in range(0, n_blocks_x):
        x = i * base.wall_img.width + base.wall_img.anchor_x
        base.walls.append(pyglet.sprite.Sprite(img=base.wall_img, x=x, y=upper_border, batch=base.field_batch))
        base.walls.append(pyglet.sprite.Sprite(img=base.wall_img, x=x, y=lower_border, batch=base.field_batch))



@base.window.event
def on_draw():
    base.window.clear()
    moving.MovingObject.batch.draw()
    base.field_batch.draw()

if __name__ == '__main__':
    pyglet.clock.schedule_interval(moving.update, 1/120.0)
    create_borders()
    pyglet.app.run()
