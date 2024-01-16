from Frames.AbstractBaseFrame import AbstractBaseFrame
import shared
from utilities.image import draw_text
from utilities.Button import Button
import pygame as pg
from utilities.level_saving import save_level
from Signals import *


class SaveLevelFrame(AbstractBaseFrame):
    def __init__(self, grid):
        self.colors = []
        self.owners = []
        for tile in grid:
            if tile.owner is not None and tile.owner not in self.owners:
                self.colors.append(tile.color)
                self.owners.append(tile.owner)

        super().__init__()
        self.grid = grid
        self.level_name = 'new_level'
        self.changing_name = False
        self.available_players = ['Игрок', 'defender', 'attacker', 'farmer']

        self.players = [3] * len(self.colors)

    def update(self):
        super().update()
        self.draw()

        for event in self.events:
            if event.type == pg.MOUSEBUTTONDOWN:
                self.set_changing_name(False)
            if event.type == pg.KEYDOWN:
                text = event.unicode
                if text.isalnum() or text == '_':
                    self.level_name += text
                if event.key == pg.K_BACKSPACE:
                    self.level_name = self.level_name[:-1]
                if event.key == pg.K_RETURN:
                    self.changing_name = False

        self.buttons.update(self.events)
        self.buttons.draw(shared.screen)

    def draw(self):
        self.draw_fon()
        draw_text(f'Название: {self.level_name}{"|" if self.changing_name else ""}', self.w * 0.046, self.h * 0.1,
                  'black', round(self.w * 0.04))
        draw_text('Игроки:', 0, self.h * 0.17, 'black', round(self.w * 0.04))
        for i in range(len(self.colors)):
            pg.draw.rect(shared.screen, self.colors[i], (
                self.w * 0.001 + (i // 7) * 0.4 * self.w, self.h * 0.23 + (i % 7) * 0.1 * self.h, int(0.04 * self.w),
                int(0.04 * self.w)))
            draw_text(self.available_players[self.players[i]], self.w * 0.045 + (i // 7) * 0.4 * self.w,
                      self.h * 0.25 + (i % 7) * 0.1 * self.h, (0, 0, 0), round(self.w * 0.04))
        draw_text('сохранить', self.w * 0.825, self.h * 0.92, 'black', round(self.w * 0.032))

    def generate_buttons(self):
        super().generate_buttons()
        change_name_button = Button(
            (self.w * 0.001, self.h * 0.1, int(0.04 * self.w), int(0.04 * self.w)),
            'change_name.png', self.buttons
        )
        change_name_button.connect(lambda: self.set_changing_name(True))
        for i in range(len(self.colors)):
            button = Button(
                (self.w * 0.001 + (i // 7) * 0.4 * self.w, self.h * 0.23 + (i % 7) * 0.1 * self.h, int(0.04 * self.w),
                 int(0.04 * self.w)),
                f'square.png', self.buttons
            )
            button.connect(lambda x=i: self.change_player(x))

        save_level_button = Button(
            (self.w * 0.78, self.h * 0.91, int(0.2 * self.w), int(0.04 * self.w)),
            'square.png', self.buttons
        )
        save_level_button.connect(self.save_level)

    def change_player(self, index):
        self.players[index] = (self.players[index] + 1) % len(self.available_players)

    def set_changing_name(self, value):
        self.changing_name = value

    def save_level(self):
        players = {}
        for i in range(len(self.colors)):
            players[self.owners[i]] = (self.available_players[self.players[i]], self.colors[i])
        save_level('data/levels/redactor', self.level_name, players, self.grid.tiles_to_string())
        raise KillFewTopFrames(2)
