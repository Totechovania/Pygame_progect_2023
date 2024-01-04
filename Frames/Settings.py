from IFrame import IFrame
from Button import Button
from utilities import draw_text, load_image, back, open_pop_window, load_json_file, change_json_file, \
    set_default_settings
import pygame as pg
import shared
from Signals import KillEntireApp


class Settings(IFrame):
    def __init__(self):
        self.w = shared.WIDTH
        self.h = shared.HEIGHT
        self.image_fon = pg.transform.scale(load_image('fon_menu.png'), (self.w, self.h))
        self.image_check = pg.transform.scale(load_image('check.png'), (self.w * 0.0145, self.h * 0.035))
        self.flag_width = False
        self.flag_height = False
        self.sound = shared.sound
        self.music = shared.music
        self.height = shared.HEIGHT
        self.width = shared.WIDTH
        self.fullscreen = shared.fullscreen
        self.buttons = pg.sprite.Group()
        self.generate_buttons()

    def update(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                raise KillEntireApp
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    back()
                if self.flag_width:
                    if len(str(self.width)) < 10:
                        if event.key == pg.K_0:
                            self.width = int(str(self.width) + '0')
                        if event.key == pg.K_1:
                            self.width = int(str(self.width) + '1')
                        if event.key == pg.K_2:
                            self.width = int(str(self.width) + '2')
                        if event.key == pg.K_3:
                            self.width = int(str(self.width) + '3')
                        if event.key == pg.K_4:
                            self.width = int(str(self.width) + '4')
                        if event.key == pg.K_5:
                            self.width = int(str(self.width) + '5')
                        if event.key == pg.K_6:
                            self.width = int(str(self.width) + '6')
                        if event.key == pg.K_7:
                            self.width = int(str(self.width) + '7')
                        if event.key == pg.K_8:
                            self.width = int(str(self.width) + '8')
                        if event.key == pg.K_9:
                            self.width = int(str(self.width) + '9')
                        if event.key == pg.K_BACKSPACE:
                            try:
                                self.width = int(str(self.width)[:-1])
                            except Exception:
                                self.width = ''
                if self.flag_height:
                    if len(str(self.height)) < 10:
                        if event.key == pg.K_0:
                            self.height = int(str(self.height) + '0')
                        if event.key == pg.K_1:
                            self.height = int(str(self.height) + '1')
                        if event.key == pg.K_2:
                            self.height = int(str(self.height) + '2')
                        if event.key == pg.K_3:
                            self.height = int(str(self.height) + '3')
                        if event.key == pg.K_4:
                            self.height = int(str(self.height) + '4')
                        if event.key == pg.K_5:
                            self.height = int(str(self.height) + '5')
                        if event.key == pg.K_6:
                            self.height = int(str(self.height) + '6')
                        if event.key == pg.K_7:
                            self.height = int(str(self.height) + '7')
                        if event.key == pg.K_8:
                            self.height = int(str(self.height) + '8')
                        if event.key == pg.K_9:
                            self.height = int(str(self.height) + '9')
                        if event.key == pg.K_BACKSPACE:
                            try:
                                self.height = int(str(self.height)[:-1])
                            except Exception:
                                self.height = ''
            if event.type == pg.KEYUP:
                if event.key == pg.K_RETURN:
                    self.flag_width = False
                    self.flag_height = False
        self.draw_fon()
        self.buttons.update(events)
        self.buttons.draw(shared.screen)

    def generate_buttons(self):
        exit_button = Button(
            (self.w * 0.958, 0, int(0.04 * self.w), int(0.04 * self.w)), 'leave_button.png', self.buttons)
        exit_button.connect(open_pop_window)

        back_button = Button((0, 0, int(0.04 * self.w), int(0.04 * self.w)), 'back.png', self.buttons)
        back_button.connect(back)

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
        set_new_settings_button.connect(
            self.set_new_settings)

        set_default_settings_button = Button((self.w * 0.375, self.h * 0.78, self.w * 0.26, self.h * 0.09),
                                             'set_default.png', self.buttons)
        set_default_settings_button.connect(set_default_settings)

    def draw_fon(self):
        shared.screen.blit(self.image_fon, (0, 0))
        pg.draw.rect(shared.screen, pg.Color('#F0FFF0'), (self.w * 0.28, self.h * 0.1, self.w * 0.42, self.h * 0.8), 0)
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

    def change_width(self):
        self.flag_width = True
        self.flag_height = False

    def change_height(self):
        self.flag_height = True
        self.flag_width = False

    def change_fullscreen_settings(self):
        if self.fullscreen:
            self.fullscreen = False
        else:
            self.fullscreen = True

    def change_volume_settings(self):
        if self.sound:
            self.sound = False
        else:
            self.sound = True

    def change_music_settings(self):
        if self.music:
            self.music = False
        else:
            self.music = True

    def set_new_settings(self):
        data = load_json_file()
        data['SOUND'] = self.sound
        data['MUSIC'] = self.music
        data['HEIGHT'] = self.height
        data['WIDTH'] = self.width
        data['FULLSCREEN'] = self.fullscreen
        change_json_file(data)
        raise KillEntireApp
