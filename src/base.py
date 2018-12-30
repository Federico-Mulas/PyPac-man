import pyglet

pyglet.resource.path = ['../resources']
pyglet.resource.reindex()

window = pyglet.window.Window()

#walls inside the game
wall_img = pyglet.resource.image("block.png")
wall_img.height = 40
wall_img.width = 40
wall_img.anchor_x = wall_img.width/2
wall_img.anchor_y = wall_img.height/2

field_batch = pyglet.graphics.Batch()

walls = []