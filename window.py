import pyglet

from preferences import preferences
import objects

from vector import Vector2

class Window(pyglet.window.Window):

    SIZE = Vector2(preferences.window.width, preferences.window.height)

    def __init__(self):
        super().__init__()  # resizable = True

        self.fps_display = pyglet.window.FPSDisplay(self)

        self.to_draw = []

        self.draw_required = False

        self.set_size(*self.SIZE)
        self.set_caption(preferences.window.title)

        pyglet.clock.schedule_interval(self.on_update, 1/preferences.window.fps)

    def add_draw_batch(self, batch):
        self.to_draw.append(batch)

    def on_draw(self, dt = 0):
        self.clear()

        for item in self.to_draw:
            item.draw()

        if preferences.window.show_fps:
            self.fps_display.draw()

        self.flip()

    EVENT_NAMES = ['on_mouse_drag']

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if hasattr(objects, 'grid'):
            objects.grid.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if hasattr(objects, 'grid'):
            objects.grid.on_mouse_scroll(x, y, scroll_x, scroll_y)

    # def on_key_press(self, symbol, modifiers):
    #     if symbol == pyglet.window.key.UP:
    #         objects.map.on_mouse_middle_drag(0, -preferences.TILE_SIZE)

    #     elif symbol == pyglet.window.key.DOWN:
    #         objects.map.on_mouse_middle_drag(0, preferences.TILE_SIZE)

    #     elif symbol == pyglet.window.key.RIGHT:
    #         objects.map.on_mouse_middle_drag(-preferences.TILE_SIZE, 0)

    #     elif symbol == pyglet.window.key.LEFT:
    #         objects.map.on_mouse_middle_drag(preferences.TILE_SIZE, 0)

    def on_update(self, dt):
        for object_name in dir(objects):
            object = getattr(objects, object_name)
            if hasattr(object, "on_update") and object is not self:
                object.on_update(dt)

        self.on_draw()

    def on_close(self):
        for object_name in dir(objects):
            object = getattr(objects, object_name)
            if hasattr(object, "on_close") and object is not self:
                object.on_close()

        self.close()


objects.window = Window()
