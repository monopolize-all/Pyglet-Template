import pyglet, random

from preferences import preferences
import objects

from vector import Vector2
from util import MyPygletSprite


class Grid:

    # On screen
    #SIZE_ON_SCREEN = Vector2(512, 512)
    SIZE_ON_SCREEN = objects.window.SIZE
    TILE_SIZE: Vector2
    TILE_COUNT_TO_DRAW: Vector2

    MOUSE_ZOOM_COEFF = 0.01
    MIN_TILE_SCALE = Vector2(0.04)
    MAX_TILE_SCALE = Vector2(1)
    TILE_SCALE = Vector2(MIN_TILE_SCALE)

    # on storage
    GRID_SIZE = Vector2(100, 100)

    def init_vars(self):
        #self.TILE_SCALE = self.TILE_SIZE[0] / GridTile.IMAGES[0].width
        grid_tile_default_image_size = Vector2(GridTile.IMAGES[0].width, GridTile.IMAGES[0].height)
        self.TILE_SIZE = grid_tile_default_image_size * self.TILE_SCALE

        self.TILE_COUNT_TO_DRAW = ((self.SIZE_ON_SCREEN // self.TILE_SIZE) + 2).as_int()  # One extra on each side as padding

    def __init__(self):
        self.init_vars()

        self.grid_batch = pyglet.graphics.Batch()
        objects.window.add_draw_batch(self.grid_batch)

        self.focus_position = self.GRID_SIZE // 2
        self.focus_position_offset = Vector2()

        self.create_grid()
        #self[50, 50] = 1
        self.make_grid_tiles()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        #print(x, y, dx, dy, buttons, modifiers)
        if buttons == 1:
            offset = Vector2(dx, dy)
            self.focus_position_offset += Vector2(dx, dy)
            tiles_crossed = (self.focus_position_offset // self.TILE_SIZE).as_int()

            if tiles_crossed.get_square_magnitude() > 0:
                self.focus_position_offset %= self.TILE_SIZE
                self.focus_position -= tiles_crossed
                self.make_grid_tiles()

            else:
                self.offset_all_grid_tiles(offset)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.TILE_SCALE -= Vector2(scroll_y * self.MOUSE_ZOOM_COEFF)
        self.TILE_SCALE = max(self.MIN_TILE_SCALE, self.TILE_SCALE)
        self.TILE_SCALE = min(self.MAX_TILE_SCALE, self.TILE_SCALE)

        for col in self.grid_tiles:
            for grid_tile in col:
                grid_tile: GridTile
                grid_tile.set_scale(self.TILE_SCALE)

        self.init_vars()
        self.make_grid_tiles()


    def offset_all_grid_tiles(self, offset):
        for col in self.grid_tiles:
            for grid_tile in col:
                grid_tile: GridTile
                grid_tile.position += offset

    def create_grid(self):
        self.grid = []
        for ix in range(self.GRID_SIZE[0]):
            self.grid.append([])
            for iy in range(self.GRID_SIZE[1]):
                grid_point_val = 0  # random.randint(0, 1)
                self.grid[ix].append(grid_point_val)

    def get_grid_array_bounds(self):
        return (0, 0), self.GRID_SIZE

    def check_if_index_within_bounds(self, index: Vector2):
        ix, iy = index

        (bminx, bminy), (bmaxx, bmaxy) = self.get_grid_array_bounds()

        if bminx < ix < bmaxx and bminy < iy < bmaxy:
            return True
        
        else:
            return False

    def __setitem__(self, index, val):
        if len(index) == 2:
            if not self.check_if_index_within_bounds(index):
                raise Exception('Trying to set grid value outside bounds')

            self.grid[index[0]][index[1]] = val

            # Below code updates the corresponding GridTile
            gtx, gty = index - self.focus_position + self.TILE_COUNT_TO_DRAW // 2

            if 0 < gtx < len(self.grid_tiles):
                if 0 < gty < len(self.grid_tiles[gtx]):
                    grid_tile: GridTile = self.grid_tiles[gtx][gty]
                    grid_tile.change_image(val)

        else:
            raise NotImplementedError

    def __getitem__(self, index):
        if len(index) == 2:
            if not self.check_if_index_within_bounds(index):
                raise Exception('Trying to get grid value outside bounds')

            return self.grid[index[0]][index[1]]

        else:
            raise NotImplementedError

    def make_grid_tiles(self):

        self.grid_tiles = []

        tcd_x, tcd_y = self.TILE_COUNT_TO_DRAW
        
        start_tile_pos = Vector2(-self.TILE_SIZE)
        tile_pos = Vector2(start_tile_pos)
        start_tile_index = self.focus_position - self.TILE_COUNT_TO_DRAW // 2
        tile_index = Vector2(start_tile_index)

        for ix in range(-tcd_x//2, tcd_x//2):
            self.grid_tiles.append([])
            for iy in range(-tcd_y//2, tcd_y//2):

                if self.check_if_index_within_bounds(tile_index):
                    grid_tile = GridTile(tile_pos, self.grid_batch, self.TILE_SCALE)
                    grid_tile.change_image(self[tile_index])
                    
                    self.grid_tiles[-1].append(grid_tile)
                
                tile_pos[1] += self.TILE_SIZE[1]
                tile_index[1] += 1

            tile_pos[0] += self.TILE_SIZE[0]
            tile_pos[1] = start_tile_pos[1]
            tile_index[0] += 1
            tile_index[1] = start_tile_index[1]

        self.offset_all_grid_tiles(self.focus_position_offset)


class GridTile(MyPygletSprite):

    IMAGES = [pyglet.resource.image('black.png'), pyglet.resource.image('white.png')]

    def __init__(self, position, batch, scale: Vector2):
        super().__init__(img=self.IMAGES[0], x=position[0], y=position[1], batch=batch)

        self.set_scale(scale)

    def change_image(self, index):
        if 0 <= index < len(self.IMAGES):
            self.image = self.IMAGES[index]
        else:
            raise Exception('Invalid image index')

    def set_scale(self, scale: Vector2):
        self.scale_x, self.scale_y = scale


objects.grid = Grid()
