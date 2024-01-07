from Frames.IFrame import IFrame
from utilities.Button import Button
from utilities.Particles import create_particles
from utilities.image import draw_text, load_image
from utilities.music import play_sound
import pygame as pg
import shared
from Signals import *
from Frames.FightMenuWindow import FightMenuWindow
from Frames.PopUpWindow import PopUpWindow
from Frames.Campany import Campany
from Frames.FightFrame import FightFrame


class ChooseMode(IFrame):
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
        self.particles.update()
        self.draw_fon()
        self.particles.draw(shared.screen)
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
        self.image_fon = pg.transform.scale(load_image('fon_menu.png'), (self.w, self.h))
        self.generate_buttons()

    def fight(self):
        play_sound('button_press.mp3')
        raise NewFrame(FightMenuWindow())

    def redactor(self):
        play_sound('button_press.mp3')
        raise NewFrame(FightFrame(1, 0))

    def campany(self):
        play_sound('button_press.mp3')
        raise NewFrame(Campany())

    def generate_buttons(self):
        exit_button = Button(
            (self.w * 0.958, 0, int(0.04 * self.w), int(0.04 * self.w)), 'leave_button.png', self.buttons)
        exit_button.connect(self.open_pop_up_window)

        back_button = Button((0, 0, int(0.04 * self.w), int(0.04 * self.w)), 'back.png', self.buttons)
        back_button.connect(self.back)

        fight_button = Button((self.w * 0.4, self.h * 0.1, int(self.w * 0.2), int(self.h * 0.19)), 'rectangle.png',
                              self.buttons)
        fight_button.connect(self.fight)

        redactor_button = Button((self.w * 0.4, self.h * 0.25, int(self.w * 0.2), int(self.h * 0.19)), 'rectangle.png',
                                 self.buttons)
        redactor_button.connect(self.redactor)

        campany_button = Button((self.w * 0.4, self.h * 0.4, int(self.w * 0.2), int(self.h * 0.19)), 'rectangle.png',
                                self.buttons)
        campany_button.connect(self.campany)

    def draw_fon(self):
        shared.screen.blit(self.image_fon, (0, 0))
        draw_text('Сражение', self.w // 2.35, self.h // 6.3, '#08E8DE', int(self.w * 0.045))
        draw_text('Редактор', self.w // 2.35, self.h // 3.25, '#08E8DE', int(self.w * 0.045))
        draw_text('Кампания', self.w // 2.35, self.h // 2.15, '#08E8DE', int(self.w * 0.045))

    def back(self):
        play_sound('button_press.mp3')
        raise KillTopFrame

    def open_pop_up_window(self):
        play_sound('button_press.mp3')
        self.draw_fon()
        self.buttons.draw(shared.screen)
        raise NewFrame(PopUpWindow(shared.screen.copy()))
