import pygame as pg
from utilities.hexagons import hexagon_from_center
from GameEngine.GameUnits.GameUnit import GameUnit


class HexTile:
    def __init__(self, x: float, y: float, radius: float, indexes: tuple[int, int],
                 color=(125, 125, 125), owner=None, game_unit=None):
        self.color = color

        self.radius = radius

        width = round(3 ** 0.5 * self.radius)
        height = round(2 * self.radius)
        self.rect = pg.Rect(x, y, width, height)

        self.center_x = x + width / 2
        self.center_y = y + height / 2

        self.indexes = indexes

        self.owner = owner
        self.game_unit = game_unit

        self.hexagon = hexagon_from_center(self.center_x, self.center_y, self.radius)

    def collide_point(self, x: float, y: float):
        return self.rect.collidepoint(x, y)

    def collide_rect(self, rect):
        return self.rect.colliderect(rect)

    def distance(self, x: float, y: float):
        return ((self.center_x - x) ** 2 + (self.center_y - y) ** 2) ** 0.5

    def draw(self, surface: pg.Surface):
        pg.draw.polygon(surface, self.color, self.hexagon)
        self.draw_stroke(surface, (0, 0, 0), round(self.radius / 20))
        if self.game_unit is not None:
            self.game_unit.draw(surface)

    def draw_stroke(self, surface: pg.Surface, color=(255, 255, 255), width=1):
        pg.draw.polygon(surface, color, self.hexagon, width)

    def set_game_unit(self, game_unit: GameUnit):
        self.game_unit = game_unit
        self.game_unit.adjust_to_tile(self)

    def set_owner(self, owner: str or None = None, color=(125, 125, 125)):
        self.owner = owner
        self.color = color


class EmptyTile(HexTile):
    def draw_stroke(self, surface: pg.Surface, color=(255, 255, 255), width=1):
        pass

    def draw(self, surface: pg.Surface):
        pass

    def set_game_unit(self, game_unit: GameUnit):
        pass
