from Frames.PopUpWindow import PopUpWindow
from Frames.IFrame import IFrame
from utilities.Button import Button
from utilities.Particles import create_particles
from utilities.image import draw_text, load_image
from utilities.music import play_sound
import pygame as pg
import shared
from Signals import *


class Campany(IFrame):
    def __init__(self):
        self.w = shared.WIDTH
        self.h = shared.HEIGHT
        self.image_fon = pg.transform.scale(load_image('fon_menu.png'), (self.w, self.h))
        self.buttons = pg.sprite.Group()
        self.particles = pg.sprite.Group()
        self.generate_buttons()

    def update(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                raise KillEntireApp
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    raise KillTopFrame
            if event.type == pg.MOUSEBUTTONDOWN:
                create_particles(pg.mouse.get_pos(), self.particles, 'coin.png')
        self.draw_fon()
        self.buttons.update(events)
        self.particles.update()
        self.particles.draw(shared.screen)
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
        self.image_fon = pg.transform.scale(load_image('fon_menu.png'), (self.w, self.h))
        self.generate_buttons()

    def go_to_first_level(self):
        pass

    def go_to_second_level(self):
        pass

    def go_to_third_level(self):
        pass

    def go_to_forth_level(self):
        pass

    def go_to_fifth_level(self):
        pass

    def generate_buttons(self):
        exit_button = Button(
            (self.w * 0.958, 0, int(0.04 * self.w), int(0.04 * self.w)), 'leave_button.png', self.buttons)
        exit_button.connect(self.open_pop_up_window)

        back_button = Button((0, 0, int(0.04 * self.w), int(0.04 * self.w)), 'back.png', self.buttons)
        back_button.connect(self.back)

        first_level_button = Button((self.w * 0.075, self.h * 0.25, int(0.08 * self.w), int(0.08 * self.w)),
                                    'square.png', self.buttons)
        first_level_button.connect(self.go_to_first_level)

        second_level_button = Button((self.w * 0.275, self.h * 0.25, int(0.08 * self.w), int(0.08 * self.w)),
                                     'square.png', self.buttons)
        second_level_button.connect(self.go_to_second_level)

        third_level_button = Button((self.w * 0.475, self.h * 0.25, int(0.08 * self.w), int(0.08 * self.w)),
                                    'square.png', self.buttons)
        third_level_button.connect(self.go_to_third_level)

        forth_level_button = Button((self.w * 0.675, self.h * 0.25, int(0.08 * self.w), int(0.08 * self.w)),
                                    'square.png', self.buttons)
        forth_level_button.connect(self.go_to_forth_level)

        fifth_level_button = Button((self.w * 0.875, self.h * 0.25, int(0.08 * self.w), int(0.08 * self.w)),
                                    'square.png', self.buttons)
        fifth_level_button.connect(self.go_to_fifth_level)

    def draw_fon(self):
        shared.screen.blit(self.image_fon, (0, 0))
        pg.draw.rect(shared.screen, pg.Color('#7FFF00'),
                     (self.w * 0.075, self.h * 0.25, int(0.08 * self.w), int(0.08 * self.w)), 0)
        draw_text('1', self.w * 0.111, self.h * 0.33, int(self.w * 0.06))
        pg.draw.rect(shared.screen, pg.Color('#FFFF00'),
                     (self.w * 0.275, self.h * 0.25, int(0.08 * self.w), int(0.08 * self.w)), 0)
        draw_text('2', self.w * 0.311, self.h * 0.33, int(self.w * 0.06))
        pg.draw.rect(shared.screen, pg.Color('#FFD700'),
                     (self.w * 0.475, self.h * 0.25, int(0.08 * self.w), int(0.08 * self.w)), 0)
        draw_text('3', self.w * 0.511, self.h * 0.33, int(self.w * 0.06))
        pg.draw.rect(shared.screen, pg.Color('#FF8C00'),
                     (self.w * 0.675, self.h * 0.25, int(0.08 * self.w), int(0.08 * self.w)), 0)
        draw_text('4', self.w * 0.711, self.h * 0.33, int(self.w * 0.06))
        pg.draw.rect(shared.screen, pg.Color('#FF4500'),
                     (self.w * 0.875, self.h * 0.25, int(0.08 * self.w), int(0.08 * self.w)), 0)
        draw_text('5', self.w * 0.911, self.h * 0.33, int(self.w * 0.06))

    def back(self):
        play_sound('button_press.mp3')
        raise KillTopFrame

    def open_pop_up_window(self):
        play_sound('button_press.mp3')
        self.draw_fon()
        self.buttons.draw(shared.screen)
        raise NewFrame(PopUpWindow(shared.screen.copy()))
