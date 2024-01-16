from Frames.AbstractBaseFrame import AbstractBaseFrame
import shared
import pygame as pg
import os
from utilities.image import draw_text
from utilities.Button import Button


class ChooseLevelFrame(AbstractBaseFrame):
    def __init__(self, load_dir='data/levels/redactor'):
        self.levels = os.listdir(load_dir)
        super().__init__()
        self.chosen = None

    def update(self):
        super().update()
        self.draw_fon()
        self.buttons.update(self.events)
        self.buttons.draw(shared.screen)
        self.draw()

    def generate_buttons(self):
        super().generate_buttons()
        for i in range(len(self.levels)):
            button = Button(((i // 10) * self.w * 0.4, self.w * 0.075 + self.w * 0.04 * (i % 10), int(0.03 * self.w), int(0.03 * self.w)),
                            'rectangle.png', self.buttons)
            button.connect(lambda x=i: self.set_chosen_level(x))
        open_level_button = Button(
            (self.w * 0.78, self.h * 0.91, int(0.2 * self.w), int(0.04 * self.w)),
            'square.png', self.buttons
        )
        open_level_button.connect(self.open_level)

    def set_chosen_level(self, level):
        self.chosen = level

    def draw(self):
        draw_text('Выбранный уровень:', 0, self.w * 0.05, (0, 0, 0), round(self.h * 0.05))
        if self.chosen is not None:
            draw_text(self.levels[self.chosen], self.w * 0.2, self.w * 0.05, (0, 0, 0), round(self.h * 0.05))
        for i in range(len(self.levels)):
            draw_text(self.levels[i], self.w * 0.05 + (i // 10) * self.w * 0.4, self.w * 0.075 + self.w * 0.04 * (i % 10), (0, 0, 0),
                      round(self.h * 0.05))
        draw_text('открыть', self.w * 0.825, self.h * 0.92, 'black', round(self.w * 0.032))

    def open_level(self):
        if self.chosen is None:
            return
        # todo
