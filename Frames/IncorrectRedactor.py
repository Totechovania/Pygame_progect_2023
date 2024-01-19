from Frames.IFrame import IFrame
from utilities.Button import Button
import pygame as pg
import shared
from Signals import KillEntireApp, KillTopFrame
from utilities.image import load_image, draw_text
import shutil


class IncorrectRedactor(IFrame):
    def __init__(self, redactor_level):
        self.w = shared.WIDTH
        self.h = shared.HEIGHT
        self.redactor_level = redactor_level[1]
        shutil.rmtree(redactor_level[0] + '/' + redactor_level[1])
        self.image_fon = pg.transform.scale(load_image('fon_menu.png'), (self.w, self.h))
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
        confirm_button_menu = Button(
            (self.w * 0.387, self.h * 0.55, self.w * 0.16, self.h * 0.15), 'rectangle.png', self.buttons)
        confirm_button_menu.connect(self.back_menu)

    def draw_fon(self):
        shared.screen.blit(self.image_fon, (0, 0))
        draw_text(
            f'{self.redactor_level} удалено. -> При создании вашей карты из редактора произошла ошибка,',
            self.w * 0.1, self.h * 0.1, '#000000', int(self.h * 0.05))
        draw_text(
            ' из-за неправильных настроек карты,'
            ' для того чтобы этого больше не повторялось прочитайте файл HowToUseRedactor.txt',
            self.w * 0.05, self.h * 0.2, '#000000', int(self.h * 0.05))
        draw_text('Вернуться', self.w * 0.42, self.h * 0.6, '#000000', int(self.h * 0.07))

    def back_menu(self):
        raise KillTopFrame
