from Frames.IFrame import IFrame
from utilities.Button import Button
from utilities.image import blur_image, draw_text
import pygame as pg
import shared
from Signals import KillEntireApp, KillTopFrame, KillFewTopFrames
from time import time


class FinalWindow(IFrame):
    def __init__(self, image, spent_money, earned_money, captured_states, winner, time_start):
        self.spent_money = spent_money
        self.earned_money = earned_money
        self.captured_states = captured_states
        self.winner = winner
        self.time_start = time_start
        self.time_now = time() - self.time_start
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
        confirm_button_menu = Button(
            (self.w * 0.518, self.h * 0.8, self.w * 0.16, self.h * 0.15), 'rectangle.png', self.buttons)
        confirm_button_menu.connect(self.back_menu)

        back_button = Button((self.w * 0.285, self.h * 0.8, self.w * 0.21, self.h * 0.15), 'rectangle.png',
                             self.buttons)
        back_button.connect(self.back)

    def draw_fon(self):
        shared.screen.blit(self.img, (0, 0))
        draw_text('Результаты:', self.w * 0.38, self.h * 0.02, '#000000', int(self.h * 0.14))
        if self.winner != 'Игрок':
            draw_text('Вы ПРОИГРАЛИ от рук бота ' + self.winner, self.w * 0.2, self.h * 0.15, '#000000',
                      int(self.h * 0.14))
        else:
            draw_text('Вы ВЫИГРАЛИ', self.w * 0.35, self.h * 0.15, '#000000', int(self.h * 0.14))
        draw_text('Потрачено денег: ' + str(self.spent_money), self.w * 0.35, self.h * 0.3, '#000000',
                  int(self.h * 0.07))
        draw_text('Заработано денег: ' + str(self.earned_money), self.w * 0.35, self.h * 0.45, '#000000',
                  int(self.h * 0.07))
        draw_text('Разрушено государств: ' + str(self.captured_states), self.w * 0.35, self.h * 0.6, '#000000',
                  int(self.h * 0.07))
        draw_text('Проведено времени в игре: ' + str(int(self.time_now)) + ' С', self.w * 0.35, self.h * 0.75,
                  '#000000',
                  int(self.h * 0.07))
        draw_text('Выйти в меню', self.w * 0.53, self.h * 0.85, '#000000', int(self.h * 0.07))
        draw_text('Вернуться на поле', self.w * 0.3, self.h * 0.85, '#000000', int(self.h * 0.07))

    def close_app(self):
        raise KillEntireApp

    def back(self):
        raise KillTopFrame

    def back_menu(self):
        raise KillFewTopFrames(4)
