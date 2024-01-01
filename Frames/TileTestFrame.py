from IFrame import IFrame
from Signals import *
import shared
from Tile import HexTile, HexGroup
import pygame as pg


class TileTestFrame(IFrame):
    def __init__(self):
        self.tiles = HexGroup()
        r = 100
        for x in range(10):
            for y in range(10):
                self.tiles.add_tile(HexTile(x * r * 3 ** 0.5 + 100 + (y % 2) * r / 2 * 3 ** 0.5, 100 + y * r * 1.5, r,))

    def update(self):
        shared.screen.fill(pg.Color('black'))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                raise KillEntireApp

        self.tiles.update()
        self.tiles.draw(shared.screen)
        pg.display.flip()
