from IFrame import IFrame
from Button import Button
from utilities import draw_text, load_image, convert_image, back
import pygame as pg
import shared
from Signals import KillEntireApp, KillTopFrame


class PopUpWindow(IFrame):
    def __init__(self, path_to_fon):
        self.w = shared.WIDTH
        self.h = shared.HEIGHT
        convert_image(path_to_fon)
        self.image_fon = pg.transform.scale(load_image(path_to_fon), (self.w, self.h))
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
        confirm_button = Button(
            (self.w * 0.518, self.h * 0.55, self.w * 0.13, self.h * 0.15), 'rectangle.png', self.buttons)
        confirm_button.connect(self.exit)

        back_button = Button((self.w * 0.335, self.h * 0.55, self.w * 0.13, self.h * 0.15), 'rectangle.png',
                             self.buttons)
        back_button.connect(back)

    def exit(self):
        raise KillEntireApp

    def draw_fon(self):
        shared.screen.blit(self.image_fon, (0, 0))
        draw_text('Выйти ?', self.w * 0.42, self.h * 0.2, '#000000', int(self.h * 0.14))
        draw_text('Выйти', self.w * 0.55, self.h * 0.6, '#000000', int(self.h * 0.07))
        draw_text('Вернуться', self.w * 0.35, self.h * 0.6, '#000000', int(self.h * 0.07))
