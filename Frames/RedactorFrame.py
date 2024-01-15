from Frames.IFrame import IFrame
import pygame as pg
from Signals import *
import shared
from GameEngine.HexGrid import HexGrid
from Frames.AbstractBaseFrame import AbstractBaseFrame


class RedactorFrame(AbstractBaseFrame):
    def __init__(self):
        super().__init__()
        self.bot_types = ['defender', 'attacker', 'farmer']
        self.w = shared.WIDTH
        self.h = shared.HEIGHT
        self.grid_rect = pg.Rect(0, round(self.w * 0.05), self.w, round(shared.HEIGHT * 0.8))

        self.grid = HexGrid.filled(10, 10, 40, self.grid_rect)

        self.grid_is_moving = False

        self.chosen = None

    def update(self):
        super().update()
        for event in self.events:
            if event.type == pg.MOUSEWHEEL:
                x, y = pg.mouse.get_pos()
                if event.y < 0:
                    self.grid.relative_scale(x, y, self.grid.scale * 0.9)
                else:
                    self.grid.relative_scale(x, y, self.grid.scale * 1.1)
            elif event.type == pg.MOUSEMOTION and pg.mouse.get_pressed()[1]:
                dx, dy = pg.mouse.get_rel()
                if self.grid_is_moving:
                    self.grid.move(dx, dy)
                else:
                    self.grid_is_moving = True
            else:
                self.grid_is_moving = False

        self.buttons.update(self.events)
        pg.draw.rect(shared.screen, (255, 255, 255), self.grid_rect) # todo переделать

        self.grid.draw_tiles()

        x, y = pg.mouse.get_pos()
        if self.grid.rect.collidepoint(x, y):
            self.chosen = self.grid.collide_point(x, y)

        if self.chosen is not None:
            self.grid.draw_tile_stroke(self.chosen, (255, 255, 255), 4)

        self.grid.draw(shared.screen)

        self.buttons.draw(shared.screen)
