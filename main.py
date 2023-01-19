import pyglet

pyglet.resource.path = ['res/images']
pyglet.resource.reindex()

import preferences, objects
import window
import grid

pyglet.app.run()
