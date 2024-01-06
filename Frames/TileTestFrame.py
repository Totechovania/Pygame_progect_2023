from GameEngine.GameUnits.GameUnit import GameUnit
from Frames.IFrame import IFrame
from Signals import *
import shared
from GameEngine.HexGrid import HexGrid
import pygame as pg
from GameEngine.Tile import HexTile, EmptyTile

from utilities.image import draw_text


class TileTestFrame(IFrame):
    def __init__(self):
        self.grid = HexGrid.filled(3, 5, 40,
                                   (20, 20, round(shared.WIDTH * 0.8), round(shared.HEIGHT * 0.8)))
        self.flag = False
        self.chosen = None

    def update(self):
        shared.screen.fill((255, 255, 255))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                raise KillEntireApp
            if event.type == pg.MOUSEBUTTONDOWN:
                clicked = self.grid.collide_point(*event.pos)
                if clicked is not None:
                    if event.button == 1:
                        if clicked.game_unit is None:
                            clicked.set_game_unit(GameUnit('back.png', 0.1))
                        else:
                            clicked.game_unit = None
                    elif event.button == 3:
                        if isinstance(clicked, EmptyTile):
                            self.grid.set_tile(clicked.indexes[0], clicked.indexes[1])
                        elif isinstance(clicked, HexTile):
                            self.grid.set_empty(clicked.indexes[0], clicked.indexes[1])

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

        self.chosen = self.grid.collide_point(*pg.mouse.get_pos())

        self.grid.draw_tiles()
        if self.chosen is not None:
            tile = self.chosen
            text = f'({tile.indexes[0]}, {tile.indexes[1]})'
            x, y = tile.center_x, tile.center_y
            draw_text(text, 0, 0, (0, 0, 0))

        if self.chosen is not None:
            self.chosen.draw_stroke(self.grid.surface)
            indexes = self.chosen.indexes
            for tile in self.grid.get_adjacent_tiles(indexes[0], indexes[1]):
                tile.draw_stroke(self.grid.surface)

        self.grid.draw(shared.screen)
