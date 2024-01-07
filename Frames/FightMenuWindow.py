from Frames.PopUpWindow import PopUpWindow
from Frames.IFrame import IFrame
from utilities.Button import Button
from utilities.Particles import create_particles
from utilities.image import load_image, draw_text
from utilities.music import play_sound
from utilities.change_settings import load_json_file, change_json_file
from Frames.FightFrame import FightFrame
import pygame as pg
import shared
from Signals import *


class FightMenuWindow(IFrame):
    def __init__(self):
        self.w = shared.WIDTH
        self.h = shared.HEIGHT
        self.image_fon = pg.transform.scale(load_image('fon_menu.png'), (self.w, self.h))
        self.buttons = pg.sprite.Group()
        self.particles = pg.sprite.Group()
        self.generate_buttons()
        self.variations = {0: '#7FFF00', 1: '#FFFF00', 2: '#FFD700', 3: '#FF8C00', 4: '#FF4500', 5: '#FF0000',
                           6: '#8B0000', 7: '#9400D3', 8: '#800080', 9: '#4B0082'}
        data = load_json_file('fight_settings.json')
        self.saved = False
        self.difficulty = data['DIFFICULTY']
        self.map_size = data['MAP_SIZE']
        self.players = data['PLAYERS']
        self.colors = data['COLORS']

    def apply_settings(self):
        self.buttons.empty()
        if shared.fullscreen:
            shared.screen = pg.display.set_mode((shared.fullscreen_w, shared.fullscreen_h), pg.FULLSCREEN)
            shared.WIDTH = shared.fullscreen_w
            shared.HEIGHT = shared.fullscreen_h
        else:
            shared.screen = pg.display.set_mode((shared.WIDTH, shared.HEIGHT))
        self.w = shared.WIDTH
        self.h = shared.HEIGHT
        self.image_fon = pg.transform.scale(load_image('fon_menu.png'), (self.w, self.h))
        self.generate_buttons()

    def update(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                raise KillEntireApp
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    raise KillTopFrame
            if event.type == pg.MOUSEBUTTONDOWN:
                create_particles(pg.mouse.get_pos(), self.particles, 'coin.png')
        self.particles.update()
        self.draw_fon()
        self.particles.draw(shared.screen)
        self.buttons.update(events)
        self.buttons.draw(shared.screen)

    def generate_buttons(self):
        exit_button = Button(
            (self.w * 0.958, 0, int(0.04 * self.w), int(0.04 * self.w)), 'leave_button.png', self.buttons)
        exit_button.connect(self.open_pop_up_window)

        back_button = Button((0, 0, int(0.04 * self.w), int(0.04 * self.w)), 'back.png', self.buttons)
        back_button.connect(self.back)

        choose_complex_button = Button((self.w * 0.15, self.h * 0.15, int(0.08 * self.w), int(0.04 * self.w)),
                                       'square.png', self.buttons)
        choose_complex_button.connect(self.complex_step)

        choose_size_button = Button((self.w * 0.15, self.h * 0.4, int(0.08 * self.w), int(0.04 * self.w)),
                                    'square.png', self.buttons)
        choose_size_button.connect(self.size_step)

        choose_players_button = Button((self.w * 0.15, self.h * 0.65, int(0.08 * self.w), int(0.04 * self.w)),
                                       'square.png', self.buttons)
        choose_players_button.connect(self.players_step)

        choose_colors_button = Button((self.w * 0.15, self.h * 0.89, int(0.08 * self.w), int(0.04 * self.w)),
                                      'square.png', self.buttons)
        choose_colors_button.connect(self.colors_step)

        save_settings_button = Button((self.w * 0.689, self.h * 0.18, int(0.17 * self.w), int(0.04 * self.w)),
                                      'square.png', self.buttons)
        save_settings_button.connect(self.save_settings)

        start_game_button = Button((self.w * 0.689, self.h * 0.58, int(0.17 * self.w), int(0.04 * self.w)),
                                   'square.png', self.buttons)
        start_game_button.connect(self.start_game)

    def draw_fon(self):
        shared.screen.blit(self.image_fon, (0, 0))

        if self.saved:
            draw_text('Сохранено!', self.w * 0.72, self.h * 0.3, 'black', int(self.w * 0.03))

        draw_text('Сложность (1 - 5)', self.w * 0.065, self.h * 0.05, 'black', int(self.w * 0.04))
        pg.draw.rect(shared.screen, pg.Color(self.variations[self.difficulty]),
                     (self.w * 0.15, self.h * 0.15, int(0.08 * self.w), int(0.04 * self.w)), 0)
        draw_text(str(self.difficulty + 1), self.w * 0.185, self.h * 0.18, int(self.w * 0.05))

        draw_text('Размер карты (1 - 4)', self.w * 0.065, self.h * 0.3, 'black', int(self.w * 0.04))
        pg.draw.rect(shared.screen, pg.Color(self.variations[self.map_size]),
                     (self.w * 0.15, self.h * 0.4, int(0.08 * self.w), int(0.04 * self.w)), 0)
        draw_text(str(self.map_size + 1), self.w * 0.185, self.h * 0.43, int(self.w * 0.05))

        draw_text('Количество игроков (1 - 4)', self.w * 0.065, self.h * 0.54, 'black', int(self.w * 0.04))
        pg.draw.rect(shared.screen, pg.Color(self.variations[self.players]),
                     (self.w * 0.15, self.h * 0.65, int(0.08 * self.w), int(0.04 * self.w)), 0)
        draw_text(str(self.players + 1), self.w * 0.185, self.h * 0.68, int(self.w * 0.05))

        draw_text('Количество цветов (2 - 9)', self.w * 0.065, self.h * 0.78, 'black', int(self.w * 0.04))
        pg.draw.rect(shared.screen, pg.Color(self.variations[self.colors]),
                     (self.w * 0.15, self.h * 0.89, int(0.08 * self.w), int(0.04 * self.w)), 0)
        draw_text(str(self.colors + 1), self.w * 0.185, self.h * 0.92, int(self.w * 0.05))

        draw_text('Сохранить', self.w * 0.7, self.h * 0.2, 'black', int(self.w * 0.04))
        draw_text('Начать', self.w * 0.725, self.h * 0.6, 'black', int(self.w * 0.04))

    def complex_step(self):
        self.saved = False
        self.difficulty = (self.difficulty + 1) % 5

    def size_step(self):
        self.saved = False
        self.map_size = (self.map_size + 1) % 4

    def players_step(self):
        self.saved = False
        self.players = (self.players + 1) % 4

    def colors_step(self):
        self.saved = False
        self.colors = (self.colors + 1) % 9
        if self.colors == 0:
            self.colors = 1

    def start_game(self):
        raise NewFrame(FightFrame(1))

    def save_settings(self):
        self.saved = True
        data = load_json_file('fight_settings.json')
        data['DIFFICULTY'] = self.difficulty
        data['MAP_SIZE'] = self.map_size
        data['PLAYERS'] = self.players
        data['COLORS'] = self.colors
        change_json_file(data, 'fight_settings.json')

    def back(self):
        play_sound('button_press.mp3')
        raise KillTopFrame

    def open_pop_up_window(self):
        play_sound('button_press.mp3')
        self.draw_fon()
        self.buttons.draw(shared.screen)
        raise NewFrame(PopUpWindow(shared.screen.copy()))
