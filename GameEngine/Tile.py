import pygame as pg
from utilities.hexagons import hexagon_from_center
from GameEngine.GameUnits.GameUnit import GameUnit


class HexTile:
    def __init__(self, x: float, y: float, radius: float, indexes: tuple[int, int],
                 color=None, owner=None, game_unit=None):
        if color is not None:
            self.color = color
        else:
            self.color = (125, 125, 125)
        self.radius = radius

        width = round(3 ** 0.5 * self.radius)
        height = round(2 * self.radius)
        self.rect = pg.Rect(x, y, width, height)

        self.center_x = x + width / 2
        self.center_y = y + height / 2

        self.indexes = indexes

        self.owner = owner
        self.game_unit = game_unit

    def collide_point(self, x: float, y: float):
        return self.rect.collidepoint(x, y)

    def collide_rect(self, rect):
        return self.rect.colliderect(rect)

    def distance(self, x: float, y: float):
        return ((self.center_x - x) ** 2 + (self.center_y - y) ** 2) ** 0.5

    def draw(self, surface: pg.Surface):
        hexagon = hexagon_from_center(self.center_x, self.center_y, self.radius)
        pg.draw.polygon(surface, self.color, hexagon,)
        pg.draw.polygon(surface, (0, 0, 0), hexagon, round(self.radius / 20))
        if self.game_unit is not None:
            self.game_unit.draw(surface)

    def draw_stroke(self, surface: pg.Surface, color=(255, 255, 255)):
        hexagon = hexagon_from_center(self.center_x, self.center_y, self.radius)
        pg.draw.polygon(surface, color, hexagon, round(self.radius / 12))

    def set_game_unit(self, game_unit: GameUnit):
        if self.game_unit is not None:
            raise ValueError("Tile already has a game unit")
        self.game_unit = game_unit
        self.game_unit.adjust_to_tile(self)


class EmptyTile(HexTile):
    def draw_stroke(self, surface: pg.Surface, color=(255, 255, 255)):
        pass

    def draw(self, surface: pg.Surface):
        pass

    def set_game_unit(self, game_unit: GameUnit):
        pass


