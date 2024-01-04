import pygame as pg
from IFrame import IFrame
from Signals import KillEntireApp, NewFrame
from utilities import draw_text, load_image, open_pop_window, back, create_particles
from Button import Button
from Frames.Settings import Settings
from Frames.ChooseMode import ChooseMode
# from AnimatedFon import AnimatedSprite
import shared


class MainMenu(IFrame):
    def __init__(self):
        self.w = shared.WIDTH
        self.h = shared.HEIGHT
        self.image_fon = pg.transform.scale(load_image('fon_menu.png'), (self.w, self.h))
        self.buttons = pg.sprite.Group()
        self.particles = pg.sprite.Group()
        self.fon = pg.sprite.Group()
        self.generate_buttons()

    def update(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                raise KillEntireApp
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    back()
            if event.type == pg.MOUSEBUTTONDOWN:
                create_particles(pg.mouse.get_pos(), self.particles, 'coin.png')
        self.draw_fon()
        self.fon.update()
        self.fon.draw(shared.screen)
        self.particles.update()
        self.buttons.update(events)
        self.particles.draw(shared.screen)
        self.buttons.draw(shared.screen)

    def settings(self):
        raise NewFrame(Settings())

    def start_button(self):
        raise NewFrame(ChooseMode())

    def draw_fon(self):
        shared.screen.blit(self.image_fon, (0, 0))
        draw_text('MyAntiyoy', self.w // 2.58, self.h // 4.25, '#00FF7F', int(self.w * 0.058))

    def generate_buttons(self):
        # AnimatedSprite(load_image("dragon.png", -1), 8, 2, self.fon)
        exit_button = Button(
            (self.w * 0.958, 0, int(0.04 * self.w), int(0.04 * self.w)), 'leave_button.png', self.buttons)
        exit_button.connect(open_pop_window)

        settings_button = Button((0, 0, int(0.04 * self.w), int(0.04 * self.w)), 'settings_button.png', self.buttons)
        settings_button.connect(self.settings)

        game_start_button = Button((self.w * 0.46, self.h * 0.5, int(0.08 * self.w), int(0.08 * self.w)),
                                   'game_start_button.png', self.buttons)
        game_start_button.connect(self.start_button)
