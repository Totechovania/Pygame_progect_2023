import random

import pygame as pg

from math import pi, sin, cos


class HexTile:
    def __init__(self, x: float, y: float, radius: float, indexes: tuple[int, int], *groups, color=None, ):
        for group in groups:
            group.add(self)
        if color is not None:
            self.color = color
        else:
            self.color = tuple(random.randint(0, 255) for _ in range(3))

        self.radius = radius

        width = round(3 ** 0.5 * self.radius)
        height = round(2 * self.radius)
        self.rect = pg.Rect(x, y, width, height)

        self.center_x = x + width / 2
        self.center_y = y + height / 2

        self.indexes = indexes

    def collide_point(self, x: float, y: float):
        return self.rect.collidepoint(x, y)

    def distance(self, x: float, y: float):
        return ((self.center_x - x) ** 2 + (self.center_y - y) ** 2) ** 0.5

    def draw(self, surface: pg.Surface):
        #pg.draw.rect(surface, (255, 255, 255, ), self.rect)

        hexagon = hexagon_from_center(self.center_x, self.center_y, self.radius)
        pg.draw.polygon(surface, self.color, hexagon,)

    def draw_stroke(self, surface: pg.Surface, color=(255, 255, 255)):
        hexagon = hexagon_from_center(self.center_x, self.center_y, self.radius)
        pg.draw.polygon(surface, color, hexagon, round(self.radius / 12))


def hexagon_from_center(center_x: float, center_y: float, radius: float) -> list[tuple[int, int]]:
    vertices = []
    start_x = 0
    start_y = radius
    for i in range(6):
        angle = pi / 3 * i
        x = start_x * cos(angle) - start_y * sin(angle)
        y = start_x * sin(angle) + start_y * cos(angle)
        vertices.append((round(x + center_x),
                         round(y + center_y)))

    return vertices


class HexGroup:
    def __init__(self):
        self.tiles = []
        self.chosen = None

    def add(self, tile: HexTile):
        self.tiles.append(tile)

    def draw(self, surface: pg.Surface):
        for tile in self.tiles:
            tile.draw(surface)
        if self.chosen is not None:
            self.chosen.draw_stroke(surface)

    def collide_point(self, x: float, y: float):
        collided = tuple(filter(lambda tile: tile.collide_point(x, y), self.tiles))
        if collided:
            return min(collided, key=lambda tile: tile.distance(x, y))
        return None


class HexGrid:
    def __init__(self, w: int, h: int, radius: float, pos: tuple[int, int] = (0, 0)):
        self.w = w
        self.h = h
        self.radius = radius
        self.tiles = []
        self.all_tiles = HexGroup()
        for i in range(h):
            self.tiles.append([])
            for j in range(w):
                self.tiles[i].append(HexTile(j * radius * 3 ** 0.5 + i % 2 * radius * 3 ** 0.5 / 2,
                                             i * radius * 1.5, radius, (i, j), self.all_tiles))

        self.surface = pg.Surface((round((w + (0.5 if h != 1 else 0)) * radius * 3 ** 0.5),
                                   round((1.5 * h + 0.5) * radius)))

        self.pos = pos

        self.scale = 1
        self.delta_pos = [0, 0]

    def draw(self, surface: pg.Surface):
        self.surface.fill((0, 0, 0))

        self.all_tiles.draw(self.surface)

        rect_w, rect_h = self.surface.get_size()
        scaled = pg.transform.scale(self.surface, (round(rect_w * self.scale), round(rect_h * self.scale)))

        self.surface.fill((0, 0, 0))

        self.surface.blit(scaled, self.delta_pos)
        surface.blit(self.surface, self.pos)

    def update(self):
        x, y = pg.mouse.get_pos()
        self.all_tiles.chosen = self.collide_point(x, y)

    def move(self, dx, dy):
        dx /= self.scale
        dy /= self.scale
        self.delta_pos[0] += dx
        self.delta_pos[1] += dy

    def relative_scale(self, x, y, scale):
        x_old, y_old = self.relative_pos(x, y)
        self.scale = min(max(scale, 0.7), 3)
        x_new, y_new = self.relative_pos(x, y)
        self.delta_pos[0] += (x_new - x_old) * self.scale
        self.delta_pos[1] += (y_new - y_old) * self.scale

    def relative_pos(self, x, y):
        x = (x - self.pos[0] - self.delta_pos[0]) / self.scale
        y = (y - self.pos[1] - self.delta_pos[1]) / self.scale

        return x, y

    def collide_point(self, x: float, y: float):
        return self.all_tiles.collide_point(*self.relative_pos(x, y))
