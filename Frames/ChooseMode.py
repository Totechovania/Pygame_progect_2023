from IFrame import IFrame
from Button import Button
from utilities.utilities import create_particles
from utilities.image import draw_text, load_image
import pygame as pg
import shared
from Signals import *
from Frames.FightMenuWindow import FightMenuWindow
from Frames.Download import Download
from Frames.Campany import Campany
from Frames.Redactor import Redactor


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

    def fight(self):
        raise NewFrame(FightMenuWindow())

    def redactor(self):
        raise NewFrame(Redactor())

    def download(self):
        raise NewFrame(Download())

    def campany(self):
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

        download_button = Button((self.w * 0.4, self.h * 0.55, int(self.w * 0.2), int(self.h * 0.19)), 'rectangle.png',
                                 self.buttons)
        download_button.connect(self.download)

        campany_button = Button((self.w * 0.4, self.h * 0.4, int(self.w * 0.2), int(self.h * 0.19)), 'rectangle.png',
                                self.buttons)
        campany_button.connect(self.campany)

    def draw_fon(self):
        shared.screen.blit(self.image_fon, (0, 0))
        draw_text('Сражение', self.w // 2.35, self.h // 6.3, '#08E8DE', int(self.w * 0.045))
        draw_text('Редактор', self.w // 2.35, self.h // 3.25, '#08E8DE', int(self.w * 0.045))
        draw_text('Кампания', self.w // 2.35, self.h // 2.15, '#08E8DE', int(self.w * 0.045))
        draw_text('Загрузить', self.w // 2.35, self.h // 1.62, '#08E8DE', int(self.w * 0.045))

    def back(self):
        raise KillTopFrame

    def open_pop_up_window(self):
        self.draw_fon()
        self.buttons.draw(shared.screen)
        raise NewFrame(PopUpWindow(shared.screen.copy()))
