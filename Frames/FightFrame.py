from GameEngine.GameUnits.Units import *
from GameEngine.GameUnits.Buildings import *

from Frames.IFrame import IFrame
from Signals import *
import shared
from utilities.MapGenerater import map_generator
import pygame as pg
from GameEngine.Tile import HexTile, EmptyTile
from utilities.Button import Button
from utilities.music import play_sound
from utilities.image import draw_text


class FightFrame(IFrame):
    def __init__(self, scale):
        self.w = shared.WIDTH
        self.h = shared.HEIGHT
        self.buttons = pg.sprite.Group()
        self.generate_buttons()
        self.grid = map_generator(scale)
        self.flag = False
        self.chosen = None
        self.choose = None

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
                        if clicked.game_unit is None:
                            if self.choose:
                                clicked.set_game_unit(self.choose)
                        else:
                            clicked.game_unit = None
                    elif event.button == 3:
                        if isinstance(clicked, EmptyTile):
                            self.grid.set_tile(clicked.indexes[0], clicked.indexes[1])
                        elif isinstance(clicked, HexTile):
                            self.grid.set_empty(clicked.indexes[0], clicked.indexes[1])
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    raise KillTopFrame
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
        self.draw()
        self.grid.draw(shared.screen)
        self.buttons.update(events)
        self.buttons.draw(shared.screen)

    def draw(self):
        draw_text('10 $', self.w * 0.185, self.h * 0.96, int(self.h * 0.9))
        draw_text('15 $', self.w * 0.285, self.h * 0.96, int(self.h * 0.9))
        draw_text('35 $', self.w * 0.385, self.h * 0.96, int(self.h * 0.9))

        draw_text('10 $', self.w * 0.51, self.h * 0.96, int(self.h * 0.9))
        draw_text('20 $', self.w * 0.61, self.h * 0.96, int(self.h * 0.9))
        draw_text('30 $', self.w * 0.71, self.h * 0.96, int(self.h * 0.9))
        draw_text('40 $', self.w * 0.81, self.h * 0.96, int(self.h * 0.9))

    def generate_buttons(self):
        exit_button = Button(
            (self.w * 0.958, 0, int(0.04 * self.w), int(0.04 * self.w)), 'leave_button.png', self.buttons)
        exit_button.connect(self.open_pop_up_window)

        back_button = Button((0, 0, int(0.04 * self.w), int(0.04 * self.w)), 'back.png', self.buttons)
        back_button.connect(self.back)

        back_move_button = Button((0, shared.HEIGHT * 0.9, int(0.04 * self.w), int(0.04 * self.w)), 'back_move.png',
                                  self.buttons)
        back_move_button.connect(self.back_move)

        next_move_button = Button((shared.WIDTH * 0.96, shared.HEIGHT * 0.9, int(0.04 * self.w), int(0.04 * self.w)),
                                  'next_move.png', self.buttons)
        next_move_button.connect(self.next_move)

        farmhouse_button = Button((shared.WIDTH * 0.175, shared.HEIGHT * 0.85, int(0.04 * self.w), int(0.04 * self.w)),
                                  'farm.png', self.buttons)
        farmhouse_button.connect(self.farm_house_chosen)

        tower_level_1 = Button((shared.WIDTH * 0.275, shared.HEIGHT * 0.85, int(0.04 * self.w), int(0.04 * self.w)),
                               'towerfirst.png', self.buttons)
        tower_level_1.connect(self.tower_level_1_chosen)

        tower_level_2 = Button((shared.WIDTH * 0.375, shared.HEIGHT * 0.86, int(0.04 * self.w), int(0.04 * self.w)),
                               'towersecond.png', self.buttons)
        tower_level_2.connect(self.tower_level_2_chosen)

        traveller_summon_button = Button(
            (shared.WIDTH * 0.5, shared.HEIGHT * 0.85, int(0.04 * self.w), int(0.04 * self.w)),
            'peasant.png', self.buttons)
        traveller_summon_button.connect(self.traveller_chosen)

        spearman_summon_button = Button(
            (shared.WIDTH * 0.6, shared.HEIGHT * 0.85, int(0.04 * self.w), int(0.04 * self.w)),
            'spearman.png', self.buttons)
        spearman_summon_button.connect(self.spearman_chosen)

        warrior_summon_button = Button(
            (shared.WIDTH * 0.7, shared.HEIGHT * 0.85, int(0.04 * self.w), int(0.04 * self.w)),
            'warrior.png', self.buttons)
        warrior_summon_button.connect(self.warrior_chosen)

        knight_summon_button = Button(
            (shared.WIDTH * 0.8, shared.HEIGHT * 0.85, int(0.04 * self.w), int(0.04 * self.w)),
            'knight.png', self.buttons)
        knight_summon_button.connect(self.knight_chosen)

    def back_move(self):
        pass

    def next_move(self):
        pass

    def farm_house_chosen(self):
        self.choose = Farm(2)

    def tower_level_1_chosen(self):
        self.choose = TowerFirst(2)

    def tower_level_2_chosen(self):
        self.choose = TowerSecond(2)

    def traveller_chosen(self):
        self.choose = Peasant(2)

    def spearman_chosen(self):
        self.choose = Spearman(2)

    def warrior_chosen(self):
        self.choose = Warrior(2)

    def knight_chosen(self):
        self.choose = Knight(2)

    def back(self):
        play_sound('button_press.mp3')
        raise KillTopFrame

    def open_pop_up_window(self):
        from Frames.PopUpWindow import PopUpWindow
        play_sound('button_press.mp3')
        raise NewFrame(PopUpWindow(shared.screen.copy()))
