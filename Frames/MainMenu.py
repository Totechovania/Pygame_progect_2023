import pygame as pg
from IFrame import IFrame
from Signals import KillEntireApp, NewFrame, KillTopFrame
from utilities import draw_text, draw_fon
from Button import Button
from Frames.Settings import Settings
from Frames.ChooseMode import ChooseMode
import shared


class MainMenu(IFrame):
    def __init__(self):
        self.w = shared.WIDTH
        self.h = shared.HEIGHT
        self.all_sprites = pg.sprite.Group()


        shared.screen.fill(pg.Color('white'))

    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                raise KillEntireApp
            if event.type == pg.MOUSEBUTTONDOWN:
                for button in shared.all_buttons_cords:
                    if button.get_rect().collidepoint(event.pos):
                        if button.get_info() == 'settings':
                            raise NewFrame(Settings())
                        if button.get_info() == 'choose_mode':
                            raise NewFrame(ChooseMode())
                        if button.get_info() == 'leave':
                            raise KillEntireApp
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            raise KillTopFrame

        self.start_window()
        self.all_sprites.draw(shared.screen)
        self.all_sprites.update()
        pg.display.flip()

    def start_window(self):
        draw_fon('fon_menu.png', self.w, self.h)
        draw_text('MyAntiyoy', self.w // 2.58, self.h // 4.25, '#00FF7F', int(self.w * 0.058))

        Button(self.all_sprites, 'game_start_button.png', self.w * 0.46, self.h * 0.5, int(0.08 * self.w),
               int(0.08 * self.w), 'choose_mode')
        Button(self.all_sprites, 'settings_button.png', 0, 0, int(0.04 * self.w), int(0.04 * self.w), 'settings')
        Button(self.all_sprites, 'leave_button.png', self.w * 0.958, 0, int(0.04 * self.w), int(0.04 * self.w), 'leave')
