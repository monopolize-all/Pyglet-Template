import math
import random

class Vector2:

    def __init__(self, x=None, y=None):
        if x is None:
            self.x = self.y = 0

        elif y is None:
            try:
                self.x, self.y = x
            except:
                self.x = self.y = x

        else:
            self.x = x
            self.y = y

    @property
    def copy(self):
        return Vector2(self.x, self.y)

    @staticmethod
    def randint(min_x, max_x, min_y, max_y):
        x = random.randint(min_x, max_x)
        y = random.randint(min_y, max_y)

        return Vector2(x, y)

    @staticmethod
    def format(other):
        """If other does not have __len__, it converts it into a list"""
        if not hasattr(other, '__len__'):
            return [other, other]
        else:
            return other

    def as_int(self):
        return Vector2(int(self.x), int(self.y))

    def __setitem__(self, key, val):
        if type(key) == int:
            if key == 0:
                self.x = val
            elif key == 1:
                self.y = val
            else:
                raise NotImplementedError
        
        else:
            raise NotImplementedError

    def __add__(self, other):
        x1, y1 = self
        x2, y2 = self.format(other)
        return Vector2(x1+x2, y1+y2)

    def __sub__(self, other):
        x1, y1 = self
        x2, y2 = self.format(other)
        return Vector2(x1-x2, y1-y2)

    def __neg__(self):
        x, y = self
        return Vector2(-x, -y)

    def __mul__(self, other):
        x1, y1 = self
        x2, y2 = self.format(other)
        return Vector2(x1*x2, y1*y2)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __mod__(self, other):
        x1, y1 = self
        x2, y2 = self.format(other)
        return Vector2(x1%x2, y1%y2)

    def __floordiv__(self, other):
        x1, y1 = self
        x2, y2 = self.format(other)
        return Vector2(x1//x2, y1//y2)

    def __truediv__(self, other):
        x1, y1 = self
        x2, y2 = self.format(other)
        return Vector2(x1/x2, y1/y2)

    def __gt__(self, other):
        x1, y1 = self
        x2, y2 = other

        if x1 > x2 and y1 > y2:
            return True

        return False

    def __ge__(self, other):
        x1, y1 = self
        x2, y2 = other

        if x1 >= x2 and y1 >= y2:
            return True

        return False

    def __eq__(self, other):
        x1, y1 = self
        x2, y2 = other

        if x1 == x2 and y1 == y2:
            return True

        return False

    @property
    def tuple(self):
        return self.x, self.y

    def __len__(self):
        return 2

    def __iter__(self):
        return iter((self.x, self.y))

    def __repr__(self):
        return str((self.x, self.y))

    def get_square_magnitude(self):
        x, y = self

        return x ** 2 + y ** 2

    def get_square_distance(self, other):
        x1, y1 = self
        x2, y2 = other

        return (x1-x2) ** 2 + (y1-y2) ** 2

    def get_angle(self):
        x, y = self  # Required direction

        if x == 0:
            angle = 90 * (1 if y > 0 else -1)
        else:
            angle = math.degrees(math.atan(y/x))

            if x < 0:
                angle += 180

        return angle

    def __getitem__(self, key):
        return self.tuple[key]
