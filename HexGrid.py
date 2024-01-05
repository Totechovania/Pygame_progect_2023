import random

import pygame as pg
from Tile import HexTile, EmptyTile
from GameUnit import GameUnit


class HexGrid:
    def __init__(self, w: int, h: int, radius: float,
                 rect: tuple[int, int, int, int] | pg.Rect,
                 grid: list[list[HexTile | EmptyTile]]):
        self.w = w
        self.h = h
        self.radius = radius

        self.rect = pg.Rect(rect)

        self.grid = grid

        surf_w = round((w + (0.5 if h != 1 else 0)) * radius * 3 ** 0.5)
        surf_h = round((1.5 * h + 0.5) * radius)
        self.surface = pg.Surface((surf_w, surf_h), pg.SRCALPHA)
        self.image = pg.Surface(self.rect.size, pg.SRCALPHA)

        self.scale = 1
        self.delta_pos = [0, 0]

        self.MAX_DELTA_X = surf_w
        self.MAX_DELTA_Y = surf_h

        self.MAX_SCALE = min(self.rect.size) / (3 * radius)
        self.MIN_SCALE = min(self.rect.bottom/(surf_h * 1.1), self.rect.right/(surf_w * 1.1))

    def draw(self, surface: pg.Surface):
        self.image.fill((0, 0, 0, 0))

        scaled = pg.transform.scale_by(self.image, 1 / self.scale)
        scaled.blit(self.surface, (self.delta_pos[0] / self.scale, self.delta_pos[1] / self.scale))
        scaled = pg.transform.scale_by(scaled, self.scale)

        self.image.blit(scaled, (0, 0))

        surface.blit(self.image, (self.rect.x, self.rect.y))

    def draw_tiles(self):
        self.surface.fill((0, 0, 0, 0))
        for tile in self:
            tile.draw(self.surface)

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

    def __getitem__(self, key) -> HexTile:
        return self.grid[key[0]][key[1]]

    def __setitem__(self, key, value):
        self.grid[key[0]][key[1]] = value

    def __iter__(self):
        for i in self.grid:
            for j in i:
                yield j

    def set_empty(self, i, j):
        x, y = get_tile_coords(i, j, self.radius)
        self[i, j] = EmptyTile(x, y,  self.radius, (i, j))

    def set_tile(self, i, j,  color=None, owner: str | None = None, game_unit: GameUnit | None = None,):
        x, y = get_tile_coords(i, j, self.radius)
        self[i, j] = HexTile(x, y,  self.radius, (i, j), color, owner, game_unit)

    def get_adjacent_indices(self, i, j):
        relevant = [[-1, 0], [0, -1], [1, 0], [0, 1]]
        if i % 2 == 0:
            other = [[-1, -1], [1, -1]]
        else:
            other = [[-1, 1], [1, 1]]
        relevant.extend(other)

        adjacent = [(i + d[0], j + d[1]) for d in relevant]
        adjacent = filter(lambda x: (0 <= x[0] < self.h) and (0 <= x[1] < self.w), adjacent)

        return adjacent

    def get_adjacent_tiles(self, i, j, empty_tiles=False):
        return filter(lambda tile: empty_tiles or not isinstance(tile, EmptyTile),
                      (self[i, j] for i, j in self.get_adjacent_indices(i, j)))

    @classmethod
    def empty(cls, w, h, radius, rect):
        grid = []

        for i in range(h):
            grid.append([])
            for j in range(w):
                x, y = get_tile_coords(i, j, radius)
                tile = EmptyTile(x, y, radius, (i, j))
                grid[i].append(tile)

        return cls(w, h, radius, rect, grid)

    @classmethod
    def filled(cls, w, h, radius, rect):
        grid = []
        for i in range(h):
            grid.append([])
            for j in range(w):
                x, y = get_tile_coords(i, j, radius)
                tile = HexTile(x, y, radius, (i, j))
                grid[i].append(tile)

        return cls(w, h, radius, rect, grid)


def get_tile_coords(i, j, radius):
    return j * radius * 3 ** 0.5 + i % 2 * radius * 3 ** 0.5 / 2, i * radius * 1.5
