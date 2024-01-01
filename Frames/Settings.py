from IFrame import IFrame
from Button import Button
from utilities import draw_text, load_image, change_music_settings, change_volume_settings
import pygame as pg
import shared
from Signals import KillEntireApp, KillTopFrame


class Settings(IFrame):
    def __init__(self):
        self.w = shared.WIDTH
        self.h = shared.HEIGHT
        self.image_fon = pg.transform.scale(load_image('fon_menu.png'), (self.w, self.h))
        self.image_check = pg.transform.scale(load_image('check.png'), (self.w * 0.0145, self.h * 0.035))
        self.buttons = pg.sprite.Group()
        self.generate_buttons()

    def update(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                raise KillEntireApp
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    raise KillTopFrame
        self.draw_fon()
        self.buttons.update(events)
        self.buttons.draw(shared.screen)

    def generate_buttons(self):
        exit_button = Button(
            (self.w * 0.958, 0, int(0.04 * self.w), int(0.04 * self.w)), 'leave_button.png', self.buttons)
        exit_button.connect(self.exit)

        back_button = Button((0, 0, int(0.04 * self.w), int(0.04 * self.w)), 'back.png', self.buttons)
        back_button.connect(self.back)

        sound_check_box = Button((self.w * 0.65, self.h * 0.2, self.w * 0.022, self.h * 0.05), 'check_box.png',
                                 self.buttons)
        sound_check_box.connect(change_volume_settings)

        music_check_box = Button((self.w * 0.65, self.h * 0.4, self.w * 0.022, self.h * 0.05), 'check_box.png',
                                 self.buttons)
        music_check_box.connect(change_music_settings)

    def exit(self):
        raise KillEntireApp

    def back(self):
        raise KillTopFrame

    def draw_fon(self):
        shared.screen.blit(self.image_fon, (0, 0))
        pg.draw.rect(shared.screen, pg.Color('#F0FFF0'), (self.w * 0.28, self.h * 0.1, self.w * 0.42, self.h * 0.8), 0)
        draw_text('Звук', self.w * 0.3, self.h * 0.2, '#000000', 100)
        draw_text('Музыка', self.w * 0.3, self.h * 0.4, '#000000', 100)
        if shared.sound:
            shared.screen.blit(self.image_check, (self.w * 0.6549, self.h * 0.208))
        if shared.music:
            shared.screen.blit(self.image_check, (self.w * 0.6549, self.h * 0.41))
