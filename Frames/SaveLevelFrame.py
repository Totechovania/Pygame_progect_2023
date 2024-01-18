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
        self.level = 0

        self.players = ['бот'] * len(self.colors)

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
        draw_text(f'Сложность: {self.level + 1}', self.w * 0.046, self.h * 0.17, 'black', round(self.w * 0.04))
        draw_text('Игроки:', 0, self.h * 0.24, 'black', round(self.w * 0.04))
        for i in range(len(self.colors)):
            pg.draw.rect(shared.screen, self.colors[i], (
                self.w * 0.001 + (i // 6) * 0.4 * self.w, self.h * 0.3 + (i % 6) * 0.1 * self.h, int(0.04 * self.w),
                int(0.04 * self.w)))
            draw_text(self.players[i], self.w * 0.045 + (i // 6) * 0.4 * self.w,
                      self.h * 0.32 + (i % 6) * 0.1 * self.h, (0, 0, 0), round(self.w * 0.04))
        draw_text('сохранить', self.w * 0.825, self.h * 0.92, 'black', round(self.w * 0.032))

    def generate_buttons(self):
        super().generate_buttons()
        change_name_button = Button(
            (self.w * 0.001, self.h * 0.1, int(0.04 * self.w), int(0.04 * self.w)),
            'change_name.png', self.buttons
        )
        change_name_button.connect(lambda: self.set_changing_name(True))
        change_level_button = Button(
            (self.w * 0.006, self.h * 0.17, int(0.035 * self.w), int(0.035 * self.w)),
            'square.png', self.buttons
        )
        change_level_button.connect(self.change_level)
        for i in range(len(self.colors)):
            button = Button(
                (self.w * 0.001 + (i // 6) * 0.4 * self.w, self.h * 0.30 + (i % 6) * 0.1 * self.h, int(0.04 * self.w),
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
        if self.players[index] == 'Игрок':
            self.players[index] = 'бот'
        else:
            self.players = ['бот'] * len(self.players)
            self.players[index] = 'Игрок'

    def set_changing_name(self, value):
        self.changing_name = value

    def change_level(self):
        self.level += 1
        self.level %= 5

    def save_level(self):
        info = {'players': 0, 'enemies': 0, 'level': 0}
        if 'Игрок' in self.players:
            info['players'] = 1
            owner = self.owners[self.players.index('Игрок')]
            for tile in self.grid:
                if tile.owner == owner:
                    tile.set_owner('Игрок', tile.color)
        info['enemies'] = len(self.players) - info['players']
        info['level'] = self.level + 1

        save_level('data/levels/redactor', self.level_name, info, self.grid.tiles_to_string())
        raise KillFewTopFrames(2)
