from Frames.PopUpWindow import PopUpWindow
from Frames.IFrame import IFrame
from utilities.Button import Button
from utilities.image import load_image
import pygame as pg
import shared
from Signals import *
from Frames.Settings import Settings


class AbstractBaseFrame(IFrame):
    def __init__(self):
        self.w = shared.WIDTH
        self.h = shared.HEIGHT
        self.image_fon = pg.transform.scale(load_image('fon_menu.png'), (self.w, self.h))
        self.buttons = pg.sprite.Group()
        self.generate_buttons()

    def apply_settings(self):
        self.buttons.empty()
        self.w = shared.WIDTH
        self.h = shared.HEIGHT
        self.image_fon = pg.transform.scale(load_image('fon_menu.png'), (self.w, self.h))
        self.generate_buttons()

    def update(self):
        self.events = pg.event.get()
        for event in self.events:
            if event.type == pg.QUIT:
                raise KillEntireApp
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    raise KillTopFrame
        self.draw_fon()

    def generate_buttons(self):
        exit_button = Button(
            (self.w * 0.958, 0, int(0.04 * self.w), int(0.04 * self.w)), 'leave_button.png', self.buttons)
        exit_button.connect(self.open_pop_up_window)

        back_button = Button((0, 0, int(0.04 * self.w), int(0.04 * self.w)), 'back.png', self.buttons)
        back_button.connect(self.back)

        settings_button = Button((self.w * 0.05, 0, int(0.04 * self.w), int(0.04 * self.w)), 'settings_button.png', self.buttons)
        settings_button.connect(self.settings)

    def settings(self):
        raise NewFrame(Settings())

    def draw_fon(self):
        shared.screen.blit(self.image_fon, (0, 0))

    def back(self):
        raise KillTopFrame

    def open_pop_up_window(self):
        raise NewFrame(PopUpWindow(shared.screen.copy()))
