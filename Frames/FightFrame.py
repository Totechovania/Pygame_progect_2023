from GameEngine.GameUnits.Units import *
from GameEngine.GameUnits.Buildings import *
from GameEngine.GameUnits.Obstacles import *
from Frames.IFrame import IFrame
from Signals import *
import shared
from utilities.MapGenerater import map_generator
import pygame as pg
from GameEngine.Tile import HexTile
from utilities.Button import Button
from utilities.image import draw_text, load_image
from Frames.FinalWindow import FinalWindow
from threading import Thread
from GameEngine.available_tiles import available_tiles
from GameEngine.available_tiles_to_set_new_unit import available_tiles_to_set_new_unit
from utilities.hexagons import hexagon_from_center
from GameEngine.HexGrid import HexGrid
from GameEngine.game import Game


class FightFrame(IFrame):
    def __init__(self, scale, enemy, players, level, campany_level=None, redactor_level=False):
        self.bot_types = ['defender', 'attacker', 'farmer']
        self.level = level
        self.w = shared.WIDTH
        self.h = shared.HEIGHT
        self.grid = None
        self.draw_fon_flag = True
        self.buttons = pg.sprite.Group()

        if redactor_level and (enemy + players):
            self.generate_redactor_level(redactor_level, enemy + players, players)
        else:
            if not players:
                self.draw_fon_flag = False
                rect = pg.Rect(0, 0, self.w, self.h)
            else:
                rect = pg.Rect(0, self.h * 0.08, self.w, self.h * 0.775)
            while not self.grid:
                self.grid, self.game = map_generator(scale, enemy, players, rect)
            for state_name in self.game.states_names:
                self.game.states[state_name]['state'].bot.level = self.game.states[state_name]['state'].bot.level[
                    str(self.level)]
        self.generate_buttons()
        self.game.game_fight_frame = self
        self.game.campany_level = campany_level
        if self.draw_fon_flag:
            self.fon_fight = pg.transform.scale(load_image('fon_fight.png'), (shared.WIDTH, shared.HEIGHT * 0.775))
        else:
            self.fon_fight = pg.transform.scale(load_image('fon_fight.png'), (shared.WIDTH, shared.HEIGHT))
        self.image_fon = pg.transform.scale(load_image('fon_menu.png'), (self.w, self.h))

        self.flag = False
        self.flag_draw = True
        self.flag_draw_gray = False
        self.chosen = None
        self.choose = None
        self.chosen_unit = None
        self.clicked_tile = None
        self.game.count_player_earnings()

    def update(self):
        if self.draw_fon_flag and self.game.draw_confirm:
            shared.screen.blit(self.image_fon, (0, 0))
            shared.screen.blit(self.fon_fight, (0, self.h * 0.08))
        else:
            shared.screen.blit(self.fon_fight, (0, 0))
        events = pg.event.get()
        if self.game.draw_confirm and self.game.current_player.owner != 'Игрок':
            if self.game.can_move:
                self.game.next_player()
            if 'Игрок' not in self.game.states_names:
                th = Thread(target=self.game.sleep, args=())
                th.start()
        for event in events:
            if event.type == pg.QUIT:
                raise KillEntireApp
            if event.type == pg.MOUSEBUTTONDOWN:
                clicked = self.grid.collide_point(*event.pos)
                if clicked is not None:
                    if event.button == 1:
                        if not clicked.game_unit or clicked.owner != 'Игрок' or (
                                clicked.owner == 'Игрок' and isinstance(clicked.game_unit, Obstacles)):
                            if isinstance(self.choose, HexTile):
                                self.game.move(self.choose, clicked)
                                self.choose = None
                                self.clicked_tile = None
                            if self.game.draw_confirm:
                                if self.choose and self.game.new_unit(clicked, self.chosen_unit[2]()):
                                    self.chosen_unit = None
                                    self.choose = None
                        elif clicked.game_unit and clicked.owner == self.game.current_player.owner and self.chosen_unit:
                            self.game.merge_units(clicked, self.chosen_unit[2])
                            self.flag_draw_gray = False
                        elif clicked.game_unit and clicked.owner == self.game.current_player.owner and self.choose and \
                                self.choose.game_unit and clicked != self.choose:
                            if type(self.choose.game_unit) == type(
                                    clicked.game_unit) and not self.choose.game_unit.moved:
                                self.game.merge_units_move(self.choose, clicked)
                                self.flag_draw_gray = False
                            self.choose = clicked
                        elif clicked.game_unit and self.game.states['Игрок']['state'].turn:
                            self.choose = clicked
                            self.chosen_unit = None
                            if isinstance(self.choose.game_unit, Unit) and not self.choose.game_unit.moved:
                                self.flag_draw_gray = True
                                self.clicked_tile = clicked
                    if event.button == 3:
                        self.chosen_unit = None
                        self.choose = None
                        self.clicked_tile = None
                        self.flag_draw_gray = False
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
            if self.grid.rect.collidepoint(*pg.mouse.get_pos()):
                dx, dy = pg.mouse.get_rel()
                if self.flag:
                    self.grid.move(dx, dy)
                else:
                    self.flag = True
        else:
            self.flag = False
        self.chosen = self.grid.collide_point(*pg.mouse.get_pos())
        self.grid.draw_tiles()

        if self.flag_draw_gray and self.clicked_tile:
            self.grid.draw_gray(available_tiles(self.grid, self.clicked_tile))

        if self.chosen_unit:
            self.grid.draw_gray(
                available_tiles_to_set_new_unit(self.grid, self.game.current_player.tiles, self.game.current_player,
                                                self.chosen_unit[2]))

        if self.chosen is not None and self.game.draw_confirm and 'Игрок' in self.game.states_names:
            list_of_your_state = []
            for i in self.game.states['Игрок']['state'].tiles:
                list_of_your_state.append(i.indexes)
            if self.chosen.indexes in list_of_your_state:
                for i in self.game.states['Игрок']['state'].tiles:
                    i.draw_stroke(self.grid.surface)
            else:
                self.chosen.draw_stroke(self.grid.surface)
        self.update_all(events)

    def update_all(self, events=None):
        shared.animated_units.update()
        self.grid.draw(shared.screen)
        pg.draw.rect(shared.screen, pg.Color('black'), self.grid.rect, round(self.h * 0.005))

        self.buttons.update(events)
        self.buttons.draw(shared.screen)
        hexagon = hexagon_from_center(self.w * 0.48, self.h * 0.89, self.h * 0.12)
        if self.draw_fon_flag and self.game.draw_confirm:
            pg.draw.polygon(shared.screen, (202, 116, 252), hexagon)
            pg.draw.polygon(shared.screen, pg.Color('black'), hexagon, round(self.h * 0.007))

        if self.game.draw_confirm and 'Игрок' in self.game.states_names:
            self.draw()
        if not self.game.draw_confirm and self.flag_draw:
            back_to_results_button = Button((0, 0, int(0.04 * self.w), int(0.04 * self.w)), 'back.png', self.buttons)
            back_to_results_button.connect(self.back_to_results)

    def draw(self):
        if self.chosen_unit:
            shared.screen.blit(self.chosen_unit[0], (self.w * 0.46, self.h * 0.8))
            draw_text(self.chosen_unit[1], self.w * 0.47, self.h * 0.9, int(self.h * 0.9))
            pg.draw.line(shared.screen, pg.Color('black'), (self.w * 0.425, self.h * 0.95),
                         (self.w * 0.535, self.h * 0.95), 5)

        shared.screen.blit(pg.transform.scale(load_image('money.png'), (self.w * 0.02, self.w * 0.02)),
                           (self.w * 0.425, self.h * 0.01))
        draw_text(str((self.game.states['Игрок']['state'].farms * 4) + 12) + ' $', self.w * 0.11, self.h * 0.96,
                  int(self.h * 0.9))
        draw_text('15 $', self.w * 0.21, self.h * 0.96, int(self.h * 0.9))
        draw_text('35 $', self.w * 0.31, self.h * 0.96, int(self.h * 0.9))

        draw_text('10 $', self.w * 0.61, self.h * 0.96, int(self.h * 0.9))
        draw_text('20 $', self.w * 0.71, self.h * 0.96, int(self.h * 0.9))
        draw_text('30 $', self.w * 0.81, self.h * 0.96, int(self.h * 0.9))
        draw_text('40 $', self.w * 0.91, self.h * 0.96, int(self.h * 0.9))

        draw_text(':  ', self.w * 0.45, self.h * 0.01, int(self.h * 0.9))

        if self.game.states['Игрок']['state'].earnings > 0:
            draw_text(f"{str(self.game.states['Игрок']['state'].money)}   " +
                      f"(+{str(self.game.states['Игрок']['state'].earnings)})", self.w * 0.46, self.h * 0.015,
                      int(self.h * 0.9))
        else:
            draw_text(f"{str(self.game.states['Игрок']['state'].money)}   " +
                      f"({str(self.game.states['Игрок']['state'].earnings)})", self.w * 0.46, self.h * 0.015,
                      int(self.h * 0.9))

    def generate_buttons(self):
        exit_button = Button(
            (self.w * 0.958, 0, int(0.04 * self.w), int(0.04 * self.w)), 'leave_button.png', self.buttons)
        exit_button.connect(self.open_pop_up_window)

        settings_button = Button((0, 0, int(0.04 * self.w), int(0.04 * self.w)), 'settings_button.png', self.buttons)
        settings_button.connect(self.back)
        if 'Игрок' in self.game.states_names:
            next_move_button = Button(
                (shared.WIDTH * 0.96, shared.HEIGHT * 0.9, int(0.04 * self.w), int(0.04 * self.w)),
                'next_move.png', self.buttons)
            next_move_button.connect(self.next_move)

            farmhouse_button = Button(
                (shared.WIDTH * 0.1, shared.HEIGHT * 0.85, int(0.04 * self.w), int(0.04 * self.w)),
                'farm.png', self.buttons)
            farmhouse_button.connect(self.farm_house_chosen)

            tower_level_1 = Button((shared.WIDTH * 0.2, shared.HEIGHT * 0.85, int(0.04 * self.w), int(0.04 * self.w)),
                                   'towerfirst.png', self.buttons)
            tower_level_1.connect(self.tower_level_1_chosen)

            tower_level_2 = Button((shared.WIDTH * 0.3, shared.HEIGHT * 0.86, int(0.04 * self.w), int(0.04 * self.w)),
                                   'towersecond.png', self.buttons)
            tower_level_2.connect(self.tower_level_2_chosen)

            traveller_summon_button = Button(
                (shared.WIDTH * 0.6, shared.HEIGHT * 0.85, int(0.04 * self.w), int(0.04 * self.w)),
                'peasant.png', self.buttons)
            traveller_summon_button.connect(self.traveller_chosen)

            spearman_summon_button = Button(
                (shared.WIDTH * 0.7, shared.HEIGHT * 0.85, int(0.04 * self.w), int(0.04 * self.w)),
                'spearman.png', self.buttons)
            spearman_summon_button.connect(self.spearman_chosen)

            warrior_summon_button = Button(
                (shared.WIDTH * 0.8, shared.HEIGHT * 0.85, int(0.04 * self.w), int(0.04 * self.w)),
                'warrior.png', self.buttons)
            warrior_summon_button.connect(self.warrior_chosen)

            knight_summon_button = Button(
                (shared.WIDTH * 0.9, shared.HEIGHT * 0.85, int(0.04 * self.w), int(0.04 * self.w)),
                'knight.png', self.buttons)
            knight_summon_button.connect(self.knight_chosen)

    def next_move(self):
        self.game.next_player()
        self.chosen_unit = None
        self.choose = None

    def farm_house_chosen(self):
        self.chosen_unit = (pg.transform.scale(load_image('farm.png'), (self.w * 0.04, self.w * 0.04)),
                            str((self.game.current_player.farms * 4) + 12) + ' $', Farm)
        self.choose = Farm()

    def tower_level_1_chosen(self):
        self.chosen_unit = (
            pg.transform.scale(load_image('towerfirst.png'), (self.w * 0.04, self.w * 0.04)), '15 $', TowerFirst)
        self.choose = TowerFirst()

    def tower_level_2_chosen(self):
        self.chosen_unit = (
            pg.transform.scale(load_image('towersecond.png'), (self.w * 0.04, self.w * 0.04)), '35 $', TowerSecond)
        self.choose = TowerSecond()

    def traveller_chosen(self):
        self.chosen_unit = (
            pg.transform.scale(load_image('peasant.png'), (self.w * 0.04, self.w * 0.04)), '10 $', Peasant)
        self.choose = Peasant('peasant32.png')

    def spearman_chosen(self):
        self.chosen_unit = (
            pg.transform.scale(load_image('spearman.png'), (self.w * 0.04, self.w * 0.04)), '20 $', Spearman)
        self.choose = Spearman('spearman32.png')

    def warrior_chosen(self):
        self.chosen_unit = (
            pg.transform.scale(load_image('warrior.png'), (self.w * 0.04, self.w * 0.04)), '30 $', Warrior)
        self.choose = Warrior('warrior32.png')

    def knight_chosen(self):
        self.chosen_unit = (
            pg.transform.scale(load_image('knight.png'), (self.w * 0.04, self.w * 0.04)), '40 $', Knight)
        self.choose = Knight('knight32.png')

    def back(self):
        from Frames.Settings import Settings
        raise NewFrame(Settings(True))

    # def back_move(self):
    #     self.grid = self.game.back_move()

    def open_pop_up_window(self):
        from Frames.PopUpWindow import PopUpWindow
        raise NewFrame(PopUpWindow(shared.screen.copy()))

    def apply_settings(self):
        self.buttons.empty()
        self.w = shared.WIDTH
        self.h = shared.HEIGHT
        self.generate_buttons()
        rect = pg.Rect(0, self.h * 0.08, self.w, self.h * 0.775)
        self.image_fon = pg.transform.scale(load_image('fon_menu.png'), (self.w, self.h))
        self.grid.resize(rect)
        self.fon_fight = pg.transform.scale(load_image('fon_fight.png'), (shared.WIDTH, shared.HEIGHT * 0.775))

    def back_to_results(self):
        if 'Игрок' in self.game.states_names:
            raise NewFrame(FinalWindow(shared.screen.copy(), self.game.states['Игрок']['spent_money'],
                                       self.game.states['Игрок']['earned_money'],
                                       self.game.states['Игрок']['captured_states'], self.game.current_player.owner,
                                       self.game.time_start, self.game.campany_level))
        else:
            raise KillTopFrame

    def generate_redactor_level(self, redactor_level, enemies, players):
        if not players:
            rect = pg.Rect(0, 0, self.w, self.h)
            self.draw_fon_flag = False
        else:
            rect = pg.Rect(0, self.h * 0.08, self.w, self.h * 0.775)

        self.grid = HexGrid.filled(0, 0, 40, rect)
        self.grid.tiles_from_string(redactor_level)
        self.game = Game(enemies, self.grid)
        for state_name in self.game.states_names:
            self.game.states[state_name]['state'].bot.level = self.game.states[state_name]['state'].bot.level[
                str(self.level)]
