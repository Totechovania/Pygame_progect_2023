import random

import pygame as pg
from Tile import HexTile, EmptyTile


class HexGrid:
    def __init__(self, w: int, h: int, radius: float, rect: tuple[int, int, int, int] | pg.Rect):
        self.w = w
        self.h = h
        self.radius = radius
        self.grid = []

        self.rect = pg.Rect(rect)

        surf_w = round((w + (0.5 if h != 1 else 0)) * radius * 3 ** 0.5)
        surf_h = round((1.5 * h + 0.5) * radius)
        self.surface = pg.Surface((surf_w, surf_h))

        self.image = pg.Surface(self.rect.size)

        for i in range(h):
            self.grid.append([])
            for j in range(w):
                x, y = self.get_tile_coords(i, j)
                tile = EmptyTile(x, y,  radius, (i, j), self.surface)
                self.grid[i].append(tile)

        self.scale = 1
        self.delta_pos = [0, 0]

        self.MAX_DELTA_X = surf_w
        self.MAX_DELTA_Y = surf_h

        self.MAX_SCALE = min(self.rect.size) / (3 * radius)
        self.MIN_SCALE = min(self.rect.bottom/(surf_h * 1.1), self.rect.right/(surf_w * 1.1))

        self.chosen = None

    def get_tile_coords(self, i, j):
        return j * self.radius * 3 ** 0.5 + i % 2 * self.radius * 3 ** 0.5 / 2, i * self.radius * 1.5

    def draw(self, surface: pg.Surface):

        self.image.fill((0, 0, 0))

        scaled = pg.transform.scale_by(self.image, 1 / self.scale)
        scaled.blit(self.surface, (self.delta_pos[0] / self.scale, self.delta_pos[1] / self.scale))
        scaled = pg.transform.scale_by(scaled, self.scale)

        self.image.blit(scaled, (0, 0))

        surface.blit(self.image, (self.rect.x, self.rect.y))

    def draw_tiles(self):
        self.surface.fill((0, 0, 0))
        for tile in self:
            tile.draw()

        if self.chosen is not None:
            self.chosen.draw_stroke()

    def update(self):
        x, y = pg.mouse.get_pos()
        self.chosen = self.collide_point(x, y)

    def move(self, dx, dy):
        self.delta_pos[0] += dx
        self.delta_pos[1] += dy

        self.delta_pos[0] = min(max(self.delta_pos[0], -self.MAX_DELTA_X), self.MAX_DELTA_X)
        self.delta_pos[1] = min(max(self.delta_pos[1], -self.MAX_DELTA_Y), self.MAX_DELTA_Y)

    def relative_scale(self, x, y, scale):
        x_old, y_old = self.relative_pos(x, y)
        self.scale = min(max(scale, self.MIN_SCALE), self.MAX_SCALE)
        x_new, y_new = self.relative_pos(x, y)
        self.delta_pos[0] += (x_new - x_old) * self.scale
        self.delta_pos[1] += (y_new - y_old) * self.scale

    def relative_pos(self, x, y):
        x = (x - self.rect.x - self.delta_pos[0]) / self.scale
        y = (y - self.rect.y - self.delta_pos[1]) / self.scale

        return x, y

    def collide_point(self, x: float, y: float):
        x, y = self.relative_pos(x, y)
        collided = tuple(filter(lambda tile: tile.collide_point(x, y), self))
        if collided:
            return min(collided, key=lambda tile: tile.distance(x, y))
        return None

    def __getitem__(self, i, j):
        return self.grid[i][j]

    def __setitem__(self, key, value):
        self.grid[key[0]][key[1]] = value

    def __iter__(self):
        for i in self.grid:
            for j in i:
                yield j

    def set_empty(self, i, j):
        x, y = self.get_tile_coords(i, j)
        self[i, j] = EmptyTile(x, y,  self.radius, (i, j), self.surface)

    def set_tile(self, i, j):
        x, y = self.get_tile_coords(i, j)
        self[i, j] = HexTile(x, y,  self.radius, (i, j), self.surface)

