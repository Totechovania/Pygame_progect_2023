from Frames.PopUpWindow import PopUpWindow
from Frames.IFrame import IFrame
from utilities.Button import Button
from utilities.Particles import create_particles
from utilities.image import load_image
from utilities.music import play_sound
import pygame as pg
import shared
from Signals import *


class FightMenuWindow(IFrame):
    def __init__(self):
        self.w = shared.WIDTH
        self.h = shared.HEIGHT
        self.image_fon = pg.transform.scale(load_image('fon_menu.png'), (self.w, self.h))
        self.buttons = pg.sprite.Group()
        self.particles = pg.sprite.Group()
        self.generate_buttons()

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
        self.particles.update()
        self.draw_fon()
        self.particles.draw(shared.screen)
        self.buttons.update(events)
        self.buttons.draw(shared.screen)

    def generate_buttons(self):
        exit_button = Button(
            (self.w * 0.958, 0, int(0.04 * self.w), int(0.04 * self.w)), 'leave_button.png', self.buttons)
        exit_button.connect(self.open_pop_up_window)

        back_button = Button((0, 0, int(0.04 * self.w), int(0.04 * self.w)), 'back.png', self.buttons)
        back_button.connect(self.back)

    def draw_fon(self):
        shared.screen.blit(self.image_fon, (0, 0))

    def back(self):
        play_sound('button_press.mp3')
        raise KillTopFrame

    def open_pop_up_window(self):
        play_sound('button_press.mp3')
        self.draw_fon()
        self.buttons.draw(shared.screen)
        raise NewFrame(PopUpWindow(shared.screen.copy()))
