import pyglet
from vector import Vector2


class MyPygletSprite(pyglet.sprite.Sprite):

    @property
    def position(self):
        """The (x, y) coordinates of the sprite, as a tuple.

        :Parameters:
            `x` : int
                X coordinate of the sprite.
            `y` : int
                Y coordinate of the sprite.
        """
        return Vector2(self._x, self._y)

    @position.setter
    def position(self, position):
        self._x, self._y = position
        self._update_position()
    