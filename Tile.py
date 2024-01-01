import random

import pygame as pg

from math import pi, sin, cos


class HexTile:
    def __init__(self, center_x: float, center_y: float, radius: float, color=None):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        if color is not None:
            self.color = color
        else:
            self.color = tuple(random.randint(0, 255) for _ in range(3))
        y = round(self.center_y - self.radius)
        x = round(self.center_x - 3 ** 0.5 * self.radius / 2)
        height = round(2 * self.radius)
        width = round(3 ** 0.5 * self.radius)
        self.rect = pg.Rect(x, y, width, height)

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

    def add_tile(self, tile: HexTile):
        self.tiles.append(tile)

    def draw(self, surface: pg.Surface):
        for tile in self.tiles:
            tile.draw(surface)
        if self.chosen is not None:
            self.chosen.draw_stroke(surface)

    def update(self):
        x, y = pg.mouse.get_pos()
        self.chosen = self.collide_point(x, y)

    def collide_point(self, x: float, y: float):
        collided = tuple(filter(lambda tile: tile.collide_point(x, y), self.tiles))
        if collided:
            return min(collided, key=lambda tile: tile.distance(x, y))
        return None
