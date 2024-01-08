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
from utilities.music import play_sound
from utilities.image import draw_text, load_image


class FightFrame(IFrame):
    def __init__(self, scale, enemy, level=1):
        self.bot_types = ['defender', 'attacker', 'farmer']
        self.w = shared.WIDTH
        self.h = shared.HEIGHT
        self.buttons = pg.sprite.Group()
        self.generate_buttons()
        self.grid = None
        с = 0
        while not self.grid:
            self.grid, self.game = map_generator(scale, enemy)
            print('краш' * с)
            с += 1
        self.flag = False
        self.chosen = None
        self.choose = None
        self.chosen_unit = None
        self.game.count_player_earnings()

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
                        print(clicked.game_unit)
                        if not clicked.game_unit or clicked.owner != 'Игрок' or (
                                clicked.owner == 'Игрок' and isinstance(clicked.game_unit, Obstacles)):
                            if isinstance(self.choose, HexTile):
                                self.game.move(self.choose, clicked)
                                self.choose = None
                            elif self.choose and (self.game.available_move(clicked) or self.check_near(clicked)) and int(
                                    self.chosen_unit[1].split(' ')[0]) <= self.game.states['Игрок']['state'].money \
                                    and self.check_defense(clicked) and self.check_unit(clicked):
                                unit = self.chosen_unit[2](2)
                                if isinstance(unit, Farm):
                                    self.game.states['Игрок']['state'].farms += 1
                                if isinstance(clicked.game_unit, Guildhall):
                                    self.game.states['Игрок']['captured_states'] += 1
                                self.game.states['Игрок']['spent_money'] += unit.cost
                                clicked.set_game_unit(self.choose)
                                clicked.color = self.game.states['Игрок']['state'].tiles[0].color
                                clicked.owner = 'Игрок'
                                if isinstance(unit, Unit):
                                    self.game.states['Игрок']['state'].earnings -= unit.pay
                                self.game.states['Игрок']['state'].new_tile(clicked)
                                self.game.states['Игрок']['state'].money -= unit.cost
                                self.chosen_unit = None
                                self.choose = None
                                self.game.count_player_earnings()
                        elif clicked.game_unit and self.game.states['Игрок']['state'].turn:
                            self.choose = clicked



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
            list_of_your_state = []
            for i in self.game.states['Игрок']['state'].tiles:
                list_of_your_state.append(i.indexes)
            if self.chosen.indexes in list_of_your_state:
                for i in self.game.states['Игрок']['state'].tiles:
                    i.draw_stroke(self.grid.surface)
            else:
                self.chosen.draw_stroke(self.grid.surface)
        self.grid.draw(shared.screen)
        self.buttons.update(events)
        self.buttons.draw(shared.screen)
        self.draw()

    def draw(self):
        if self.chosen_unit:
            shared.screen.blit(self.chosen_unit[0], (self.w * 0.46, self.h * 0.8))
            draw_text(self.chosen_unit[1], self.w * 0.47, self.h * 0.9, int(self.h * 0.9))
            pg.draw.line(shared.screen, pg.Color('black'), (self.w * 0.425, self.h * 0.95),
                         (self.w * 0.535, self.h * 0.95), 5)

        shared.screen.blit(pg.transform.scale(load_image('money.png'), (self.w * 0.02, self.w * 0.02)),
                           (self.w * 0.425, self.h * 0.01))

        draw_text('12 $', self.w * 0.11, self.h * 0.96, int(self.h * 0.9))
        draw_text('15 $', self.w * 0.21, self.h * 0.96, int(self.h * 0.9))
        draw_text('35 $', self.w * 0.31, self.h * 0.96, int(self.h * 0.9))

        draw_text('10 $', self.w * 0.61, self.h * 0.96, int(self.h * 0.9))
        draw_text('20 $', self.w * 0.71, self.h * 0.96, int(self.h * 0.9))
        draw_text('30 $', self.w * 0.81, self.h * 0.96, int(self.h * 0.9))
        draw_text('40 $', self.w * 0.91, self.h * 0.96, int(self.h * 0.9))

        draw_text(':  ', self.w * 0.45, self.h * 0.01, int(self.h * 0.9))
        draw_text(str(self.game.states['Игрок']['state'].money), self.w * 0.46, self.h * 0.016, int(self.h * 0.9))

        if self.game.states['Игрок']['state'].earnings > 0:
            draw_text(f"(+{str(self.game.states['Игрок']['state'].earnings)})", self.w * 0.5, self.h * 0.01,
                      int(self.h * 0.9))
        else:
            draw_text(f"({str(self.game.states['Игрок']['state'].earnings)})", self.w * 0.5, self.h * 0.01,
                      int(self.h * 0.9))

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

        farmhouse_button = Button((shared.WIDTH * 0.1, shared.HEIGHT * 0.85, int(0.04 * self.w), int(0.04 * self.w)),
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

    def back_move(self):
        try:
            shared.operational_list.pop()
        except IndexError:
            pass

    def check_near(self, clicked):
        indexes = clicked.indexes
        access = False
        for tile in self.grid.get_adjacent_tiles((indexes[0], indexes[1])):
            if tile.owner == 'Игрок':
                access = True
        return access

    def check_defense(self, clicked):
        unit = self.chosen_unit[2](2)
        if clicked.game_unit:
            if clicked.game_unit.power < unit.power:
                indexes = clicked.indexes
                access = True
                for tile in self.grid.get_adjacent_tiles((indexes[0], indexes[1])):
                    if tile.game_unit:
                        if tile.game_unit.power > unit.power:
                            if tile.owner != 'Игрок' and not isinstance(tile.game_unit, Rock):
                                access = False
                return access
            return False
        indexes = clicked.indexes
        access = True
        for tile in self.grid.get_adjacent_tiles((indexes[0], indexes[1])):
            if tile.game_unit:
                if tile.game_unit.power > unit.power:
                    if tile.owner != 'Игрок' and not isinstance(tile.game_unit, Rock):
                        access = False
        return access

    def check_unit(self, clicked):
        if not issubclass(self.chosen_unit[2], Building) or clicked.owner == 'Игрок':
            return True
        return False

    def next_move(self):
        self.game.states['Игрок']['earned_money'] += self.game.states['Игрок']['state'].earnings
        for _ in range(self.game.players):
            self.game.next_player()
            self.choose = None

    def farm_house_chosen(self):
        self.chosen_unit = (pg.transform.scale(load_image('farm.png'), (self.w * 0.04, self.w * 0.04)), '12 $', Farm)
        self.choose = Farm(2)

    def tower_level_1_chosen(self):
        self.chosen_unit = (
            pg.transform.scale(load_image('towerfirst.png'), (self.w * 0.04, self.w * 0.04)), '15 $', TowerFirst)
        self.choose = TowerFirst(2)

    def tower_level_2_chosen(self):
        self.chosen_unit = (
            pg.transform.scale(load_image('towersecond.png'), (self.w * 0.04, self.w * 0.04)), '35 $', TowerSecond)
        self.choose = TowerSecond(2)

    def traveller_chosen(self):
        self.chosen_unit = (
            pg.transform.scale(load_image('peasant.png'), (self.w * 0.04, self.w * 0.04)), '10 $', Peasant)
        self.choose = Peasant(2)

    def spearman_chosen(self):
        self.chosen_unit = (
            pg.transform.scale(load_image('spearman.png'), (self.w * 0.04, self.w * 0.04)), '20 $', Spearman)
        self.choose = Spearman(2)

    def warrior_chosen(self):
        self.chosen_unit = (
            pg.transform.scale(load_image('warrior.png'), (self.w * 0.04, self.w * 0.04)), '30 $', Warrior)
        self.choose = Warrior(2)

    def knight_chosen(self):
        self.chosen_unit = (
            pg.transform.scale(load_image('knight.png'), (self.w * 0.04, self.w * 0.04)), '40 $', Knight)
        self.choose = Knight(2)

    def back(self):
        play_sound('button_press.mp3')
        raise KillTopFrame

    def open_pop_up_window(self):
        from Frames.PopUpWindow import PopUpWindow
        play_sound('button_press.mp3')
        raise NewFrame(PopUpWindow(shared.screen.copy()))
