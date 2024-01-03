import random

import pygame as pg
from utilities import hexagon_from_center


class HexTile:
    def __init__(self, x: float, y: float, radius: float, indexes: tuple[int, int], surface: pg.Surface,  color=None,):
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

        self.surface = surface

    def collide_point(self, x: float, y: float):
        return self.rect.collidepoint(x, y)

    def collide_rect(self, rect):
        return self.rect.colliderect(rect)

    def distance(self, x: float, y: float):
        return ((self.center_x - x) ** 2 + (self.center_y - y) ** 2) ** 0.5

    def draw(self):
        hexagon = hexagon_from_center(self.center_x, self.center_y, self.radius)
        pg.draw.polygon(self.surface, self.color, hexagon,)

    def draw_stroke(self, color=(255, 255, 255)):
        hexagon = hexagon_from_center(self.center_x, self.center_y, self.radius)
        pg.draw.polygon(self.surface, color, hexagon, round(self.radius / 12))


class EmptyTile(HexTile):
    def draw_stroke(self, color=(255, 255, 255)):
        pass

    def draw(self):
        pass


