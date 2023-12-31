from Frames.IFrame import IFrame
from utilities.Button import Button
from utilities.image import blur_image, draw_text
from utilities.music import play_sound
import pygame as pg
import shared
from Signals import KillEntireApp, KillTopFrame


class PopUpWindow(IFrame):
    def __init__(self, image):
        self.w = shared.WIDTH
        self.h = shared.HEIGHT
        self.img = blur_image(image)
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
        self.generate_buttons()

    def generate_buttons(self):
        confirm_button = Button(
            (self.w * 0.518, self.h * 0.55, self.w * 0.13, self.h * 0.15), 'rectangle.png', self.buttons)
        confirm_button.connect(self.close_app)

        back_button = Button((self.w * 0.335, self.h * 0.55, self.w * 0.13, self.h * 0.15), 'rectangle.png',
                             self.buttons)
        back_button.connect(self.back)

    def draw_fon(self):
        shared.screen.blit(self.img, (0, 0))
        draw_text('Выйти ?', self.w * 0.42, self.h * 0.2, '#000000', int(self.h * 0.14))
        draw_text('Выйти', self.w * 0.55, self.h * 0.6, '#000000', int(self.h * 0.07))
        draw_text('Вернуться', self.w * 0.35, self.h * 0.6, '#000000', int(self.h * 0.07))

    def close_app(self):
        play_sound('button_press.mp3')
        raise KillEntireApp

    def back(self):
        play_sound('button_press.mp3')
        raise KillTopFrame

