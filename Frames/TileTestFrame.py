from IFrame import IFrame
from Signals import *
import shared
from Tile import HexGrid
import pygame as pg


class TileTestFrame(IFrame):
    def __init__(self):
        self.grid = HexGrid(40, 40, 20, (100, 100))
        self.flag = False

    def update(self):

        shared.screen.fill((255, 255, 255))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                raise KillEntireApp
            if event.type == pg.MOUSEWHEEL:
                x, y = pg.mouse.get_pos()
                if event.y < 0:
                    self.grid.relative_scale(x, y, self.grid.scale * 0.9)
                else:
                    self.grid.relative_scale(x, y, self.grid.scale * 1.1)

        if pg.mouse.get_pressed()[1]:
            dx, dy = pg.mouse.get_rel()
            if self.flag:
                self.grid.move(dx, dy)
            else:
                self.flag = True
        else:
            self.flag = False
        self.grid.update()
        self.grid.draw(shared.screen)
