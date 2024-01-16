from Frames.IFrame import IFrame
from utilities.Button import Button
from utilities.image import blur_image, draw_text
import pygame as pg
import shared
from Signals import KillEntireApp, KillTopFrame, KillFewTopFrames


class PopUpWindow(IFrame):
    def __init__(self, image, in_game=False):
        self.in_game = in_game
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
        self.w = shared.WIDTH
        self.h = shared.HEIGHT
        self.generate_buttons()

    def generate_buttons(self):
        if self.in_game:
            confirm_button_menu = Button(
                (self.w * 0.518, self.h * 0.55, self.w * 0.16, self.h * 0.15), 'rectangle.png', self.buttons)
            confirm_button_menu.connect(self.back_menu)
        else:
            confirm_button = Button(
                (self.w * 0.518, self.h * 0.55, self.w * 0.13, self.h * 0.15), 'rectangle.png', self.buttons)
            confirm_button.connect(self.close_app)

        back_button = Button((self.w * 0.335, self.h * 0.55, self.w * 0.13, self.h * 0.15), 'rectangle.png',
                             self.buttons)
        back_button.connect(self.back)

    def draw_fon(self):
        shared.screen.blit(self.img, (0, 0))
        if self.in_game:
            draw_text('Выйти из боя?', self.w * 0.38, self.h * 0.2, '#000000', int(self.h * 0.14))
            draw_text('(Прогресс не сохранится!)', self.w * 0.44, self.h * 0.3, '#000000', int(self.h * 0.05))
            draw_text('Выйти в меню', self.w * 0.53, self.h * 0.6, '#000000', int(self.h * 0.07))
        else:
            draw_text('Выйти ?', self.w * 0.42, self.h * 0.2, '#000000', int(self.h * 0.14))
            draw_text('Выйти', self.w * 0.55, self.h * 0.6, '#000000', int(self.h * 0.07))
        draw_text('Вернуться', self.w * 0.35, self.h * 0.6, '#000000', int(self.h * 0.07))

    def close_app(self):
        raise KillEntireApp

    def back(self):
        raise KillTopFrame

    def back_menu(self):
        raise KillFewTopFrames(4)
