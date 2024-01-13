from Frames.PopUpWindow import PopUpWindow
from Frames.IFrame import IFrame
from utilities.Button import Button
from utilities.change_settings import load_json_file, change_json_file, get_size
from utilities.Particles import create_particles
from utilities.image import draw_text, load_image
from utilities.music import play_sound, play_background_music
import pygame as pg
import shared
from Signals import *


class Settings(IFrame):
    def __init__(self, in_game=False):
        self.in_game = in_game
        self.w = shared.WIDTH
        self.h = shared.HEIGHT
        self.image_fon = pg.transform.scale(load_image('fon_menu.png'), (self.w, self.h))
        self.image_check = pg.transform.scale(load_image('check.png'), (self.w * 0.0145, self.h * 0.035))
        self.flag_width = False
        self.flag_height = False
        self.sound = shared.sound
        self.music = shared.music
        size = get_size()
        self.height = str(size[1])
        self.width = str(size[0])
        self.fullscreen = shared.fullscreen
        self.buttons = pg.sprite.Group()
        self.particles = pg.sprite.Group()
        self.generate_buttons()

    def apply_settings(self):
        self.buttons.empty()
        self.fullscreen = shared.fullscreen

        if shared.fullscreen:
            shared.screen = pg.display.set_mode((shared.fullscreen_w, shared.fullscreen_h), pg.FULLSCREEN)
            shared.WIDTH = shared.fullscreen_w
            shared.HEIGHT = shared.fullscreen_h
        else:
            shared.screen = pg.display.set_mode((shared.WIDTH, shared.HEIGHT))

        self.w = shared.WIDTH
        self.h = shared.HEIGHT
        self.image_fon = pg.transform.scale(load_image('fon_menu.png'), (self.w, self.h))
        self.image_check = pg.transform.scale(load_image('check.png'), (self.w * 0.0145, self.h * 0.035))
        self.flag_width = False
        self.flag_height = False
        self.sound = shared.sound
        self.music = shared.music
        play_background_music("music.mp3")
        self.generate_buttons()

    def update(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                raise KillEntireApp
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    raise KillTopFrame
                if self.flag_width:
                    if len(self.width) < 10:
                        if event.key == pg.K_0:
                            self.redraw_marker(self.width, '0')
                        if event.key == pg.K_1:
                            self.redraw_marker(self.width, '1')
                        if event.key == pg.K_2:
                            self.redraw_marker(self.width, '2')
                        if event.key == pg.K_3:
                            self.redraw_marker(self.width, '3')
                        if event.key == pg.K_4:
                            self.redraw_marker(self.width, '4')
                        if event.key == pg.K_5:
                            self.redraw_marker(self.width, '5')
                        if event.key == pg.K_6:
                            self.redraw_marker(self.width, '6')
                        if event.key == pg.K_7:
                            self.redraw_marker(self.width, '7')
                        if event.key == pg.K_8:
                            self.redraw_marker(self.width, '8')
                        if event.key == pg.K_9:
                            self.redraw_marker(self.width, '9')
                    if event.key == pg.K_BACKSPACE:
                        try:
                            self.width = self.width[:-2]
                            self.width += '|'
                        except Exception:
                            self.width = ''
                if self.flag_height:
                    if len(self.height) < 10:
                        if event.key == pg.K_0:
                            self.redraw_marker(self.height, '0')
                        if event.key == pg.K_1:
                            self.redraw_marker(self.height, '1')
                        if event.key == pg.K_2:
                            self.redraw_marker(self.height, '2')
                        if event.key == pg.K_3:
                            self.redraw_marker(self.height, '3')
                        if event.key == pg.K_4:
                            self.redraw_marker(self.height, '4')
                        if event.key == pg.K_5:
                            self.redraw_marker(self.height, '5')
                        if event.key == pg.K_6:
                            self.redraw_marker(self.height, '6')
                        if event.key == pg.K_7:
                            self.redraw_marker(self.height, '7')
                        if event.key == pg.K_8:
                            self.redraw_marker(self.height, '8')
                        if event.key == pg.K_9:
                            self.redraw_marker(self.height, '9')
                    if event.key == pg.K_BACKSPACE:
                        try:
                            self.height = self.height[:-2]
                            self.height += '|'
                        except Exception:
                            self.height = ''
            if event.type == pg.KEYUP:
                if event.key == pg.K_RETURN:
                    self.flag_width = False
                    self.flag_height = False
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

        sound_check_box = Button((self.w * 0.65, self.h * 0.175, self.w * 0.022, self.h * 0.05), 'check_box.png',
                                 self.buttons)
        sound_check_box.connect(self.change_volume_settings)

        music_check_box = Button((self.w * 0.65, self.h * 0.275, self.w * 0.022, self.h * 0.05), 'check_box.png',
                                 self.buttons)
        music_check_box.connect(self.change_music_settings)

        fullscreen_check_box = Button((self.w * 0.65, self.h * 0.375, self.w * 0.022, self.h * 0.05), 'check_box.png',
                                      self.buttons)
        fullscreen_check_box.connect(self.change_fullscreen_settings)

        width_write_box = Button((self.w * 0.48, self.h * 0.45, self.w * 0.175, self.h * 0.1), 'set_default.png',
                                 self.buttons)
        width_write_box.connect(self.change_width)

        height_write_box = Button((self.w * 0.48, self.h * 0.55, self.w * 0.175, self.h * 0.1), 'set_default.png',
                                  self.buttons)
        height_write_box.connect(self.change_height)

        set_new_settings_button = Button((self.w * 0.375, self.h * 0.68, self.w * 0.26, self.h * 0.09),
                                         'set_default.png', self.buttons)
        set_new_settings_button.connect(self.set_new_settings)

        set_default_settings_button = Button((self.w * 0.375, self.h * 0.78, self.w * 0.26, self.h * 0.09),
                                             'set_default.png', self.buttons)
        set_default_settings_button.connect(self.set_default_settings)

        if self.in_game:
            back_menu = Button((self.w * 0.375, self.h * 0.88, self.w * 0.26, self.h * 0.09),
                               'set_default.png', self.buttons)
            back_menu.connect(self.back_menu)

    def draw_fon(self):
        shared.screen.blit(self.image_fon, (0, 0))
        if self.in_game:
            pg.draw.rect(shared.screen, pg.Color('#F0FFF0'),
                         (self.w * 0.28, self.h * 0.1, self.w * 0.42, self.h * 0.88), 0)
            draw_text('Вернуться в меню', self.w * 0.4, self.h * 0.9, '#000000', int(self.w * 0.03))
        else:
            pg.draw.rect(shared.screen, pg.Color('#F0FFF0'), (self.w * 0.28, self.h * 0.1, self.w * 0.42, self.h * 0.8),
                         0)

        draw_text('Звук', self.w * 0.3, self.h * 0.175, '#000000', int(self.w * 0.03))
        draw_text('Музыка', self.w * 0.3, self.h * 0.275, '#000000', int(self.w * 0.03))
        draw_text('Полный экран', self.w * 0.3, self.h * 0.375, '#000000', int(self.w * 0.03))
        draw_text('Сбросить настройки', self.w * 0.4, self.h * 0.8, '#000000', int(self.w * 0.03))
        draw_text('Ширина экрана', self.w * 0.3, self.h * 0.475, '#000000', int(self.w * 0.03))
        draw_text('Высота экрана', self.w * 0.3, self.h * 0.575, '#000000', int(self.w * 0.03))
        draw_text('Сохранить настройки', self.w * 0.4, self.h * 0.7, '#000000', int(self.w * 0.03))
        draw_text(str(self.width), self.w * 0.49, self.h * 0.475, '#000000', int(self.w * 0.03))
        draw_text(str(self.height), self.w * 0.49, self.h * 0.575, '#000000', int(self.w * 0.03))
        if self.sound:
            shared.screen.blit(self.image_check, (self.w * 0.6549, self.h * 0.18))
        if self.music:
            shared.screen.blit(self.image_check, (self.w * 0.6549, self.h * 0.28))
        if self.fullscreen:
            shared.screen.blit(self.image_check, (self.w * 0.6549, self.h * 0.38))
        if self.flag_width:
            draw_text('Сохранить настройки', self.w * 0.4, self.h * 0.7, '#000000', int(self.w * 0.03))
        if self.flag_height:
            draw_text('Сохранить настройки', self.w * 0.4, self.h * 0.7, '#000000', int(self.w * 0.03))

    def change_width(self):
        play_sound('button_press.mp3')
        self.flag_width = True
        self.flag_height = False
        if str(self.height)[-1] == '|':
            self.height = str(self.height)[:-1]
        if str(self.width)[-1] != '|':
            self.width = str(self.width) + '|'

    def change_height(self):
        play_sound('button_press.mp3')
        self.flag_height = True
        self.flag_width = False
        if str(self.width)[-1] == '|':
            self.width = str(self.width)[:-1]
        if str(self.height)[-1] != '|':
            self.height = str(self.height) + '|'

    def redraw_marker(self, line, number):
        if line == self.height:
            self.height = str(self.height)[:-1]
            self.height = str(self.height) + number
            self.height = str(self.height) + '|'

        if line == self.width:
            self.width = str(self.width[:-1])
            self.width = str(self.width) + number
            self.width = str(self.width) + '|'


    def change_fullscreen_settings(self):
        play_sound('button_press.mp3')
        if self.fullscreen:
            self.fullscreen = False
        else:
            self.fullscreen = True

    def change_volume_settings(self):
        play_sound('button_press.mp3')
        if self.sound:
            self.sound = False
        else:
            self.sound = True

    def change_music_settings(self):
        play_sound('button_press.mp3')
        if self.music:
            self.music = False
        else:
            self.music = True

    def back_menu(self):
        raise NewFrame(PopUpWindow(shared.screen.copy(), True))

    def set_new_settings(self):
        play_sound('button_press.mp3')
        data = load_json_file('settings.json')
        if str(self.height)[-1] == '|':
            self.height = str(self.height)[:-1]
        if str(self.width)[-1] == '|':
            self.width = str(self.width)[:-1]
        if not (500 < int(self.width) < shared.fullscreen_w):
            self.width = int(shared.fullscreen_w * 0.55)
        if not (300 < int(self.height) < shared.fullscreen_h):
            self.height = int(shared.fullscreen_h * 0.581)
        data['SOUND'] = self.sound
        data['MUSIC'] = self.music
        data['HEIGHT'] = int(self.height)
        data['WIDTH'] = int(self.width)
        data['FULLSCREEN'] = self.fullscreen
        change_json_file(data, 'settings.json')
        shared.WIDTH = int(self.width)
        shared.HEIGHT = int(self.height)
        shared.music = self.music
        shared.sound = self.sound
        shared.fullscreen = self.fullscreen
        raise ApplySettings

    def set_default_settings(self):
        play_sound('button_press.mp3')
        data = load_json_file('settings.json')
        data['SOUND'] = True
        data['MUSIC'] = True
        data['HEIGHT'] = int(shared.fullscreen_h * 0.55)
        data['WIDTH'] = int(shared.fullscreen_w * 0.581)
        data['FULLSCREEN'] = True
        change_json_file(data, 'settings.json')
        shared.WIDTH = int(shared.fullscreen_w * 0.581)
        shared.HEIGHT = int(shared.fullscreen_h * 0.55)
        shared.music = True
        shared.sound = True
        shared.fullscreen = True
        self.sound = True
        self.music = True
        self.fullscreen = True
        self.width = int(shared.fullscreen_w * 0.581)
        self.height = int(shared.fullscreen_h * 0.55)
        raise ApplySettings

    def back(self):
        play_sound('button_press.mp3')
        raise KillTopFrame

    def open_pop_up_window(self):
        play_sound('button_press.mp3')
        raise NewFrame(PopUpWindow(shared.screen.copy()))
