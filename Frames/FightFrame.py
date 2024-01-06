from GameEngine.GameUnits.GameUnit import GameUnit
from Frames.IFrame import IFrame
from Signals import *
import shared
from utilities.MapGenerater import map_generator
from GameEngine.HexGrid import HexGrid
import pygame as pg
from GameEngine.Tile import HexTile, EmptyTile
from utilities.Button import Button
from utilities.music import play_sound


class FightFrame(IFrame):
    def __init__(self):
        self.w = shared.WIDTH
        self.h = shared.HEIGHT
        self.buttons = pg.sprite.Group()
        self.generate_buttons()
        self.grid = map_generator(1)
        self.flag = False
        self.chosen = None

    def update(self):
        shared.screen.fill((255, 255, 255))
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                raise KillEntireApp
            if event.type == pg.MOUSEBUTTONDOWN:
                clicked = self.grid.collide_point(*event.pos)
                if clicked is not None:
                    if event.button == 1:
                        self.grid = map_generator(1)
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
            self.chosen.draw_stroke(self.grid.surface)
            indexes = self.chosen.indexes
            for tile in self.grid.get_adjacent_tiles(indexes[0], indexes[1]):
                tile.draw_stroke(self.grid.surface)
        self.grid.draw(shared.screen)
        self.buttons.update(events)
        self.buttons.draw(shared.screen)

    def generate_buttons(self):
        exit_button = Button(
            (self.w * 0.958, 0, int(0.04 * self.w), int(0.04 * self.w)), 'leave_button.png', self.buttons)
        exit_button.connect(self.open_pop_up_window)

        back_button = Button((0, 0, int(0.04 * self.w), int(0.04 * self.w)), 'back.png', self.buttons)
        back_button.connect(self.back)


    def back(self):
        play_sound('button_press.mp3')
        raise KillTopFrame

    def open_pop_up_window(self):
        from Frames.PopUpWindow import PopUpWindow
        play_sound('button_press.mp3')
        raise NewFrame(PopUpWindow(shared.screen.copy()))
