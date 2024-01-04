import pygame as pg

from Frames.PopUpWindow import PopUpWindow
from IFrame import IFrame
from Signals import *
from utilities import draw_text, load_image, play_sound
from Button import Button
from Frames.Settings import Settings
from Frames.ChooseMode import ChooseMode
import shared


class MainMenu(IFrame):
    def __init__(self):
        self.w = shared.WIDTH
        self.h = shared.HEIGHT
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
        self.buttons.update(events)

        self.draw_fon()
        self.buttons.draw(shared.screen)

    def settings(self):
        play_sound('button_press.mp3')
        raise NewFrame(Settings())



    def start_button(self):
        play_sound('button_press.mp3')
        raise NewFrame(ChooseMode())

    def draw_fon(self):
        shared.screen.blit(self.image_fon, (0, 0))
        draw_text('MyAntiyoy', self.w // 2.58, self.h // 4.25, '#00FF7F', int(self.w * 0.058))

    def generate_buttons(self):
        exit_button = Button(
            (self.w * 0.958, 0, int(0.04 * self.w), int(0.04 * self.w)), 'leave_button.png', self.buttons)
        exit_button.connect(self.open_pop_up_window)

        settings_button = Button((0, 0, int(0.04 * self.w), int(0.04 * self.w)), 'settings_button.png', self.buttons)
        settings_button.connect(self.settings)

        game_start_button = Button((self.w * 0.46, self.h * 0.5, int(0.08 * self.w), int(0.08 * self.w)),
                                   'game_start_button.png', self.buttons)
        game_start_button.connect(self.start_button)

    def close_app(self):
        play_sound('button_press.mp3')
        raise KillEntireApp

    def back(self):
        play_sound('button_press.mp3')
        raise KillTopFrame

    def open_pop_up_window(self):
        self.draw_fon()
        play_sound('button_press.mp3')
        self.buttons.draw(shared.screen)
        raise NewFrame(PopUpWindow(shared.screen.copy()))
