from IFrame import IFrame
from Button import Button
#from RadioButton import RadioButton
from utilities import draw_fon, draw_text
import pygame as pg
import shared
from Signals import KillEntireApp, KillTopFrame


class Settings(IFrame):
    def __init__(self):
        self.w = shared.WIDTH
        self.h = shared.HEIGHT
        self.all_sprites = pg.sprite.Group()
        self.draw_settings()

    def draw_settings(self):
        draw_fon('fon_menu.png', self.w, self.h)

        pg.draw.rect(shared.screen, pg.Color('#F0FFF0'), (self.w * 0.28, self.h * 0.1, self.w * 0.42, self.h * 0.8), 0)
        draw_text('Звук', self.w * 0.3, self.h * 0.2, '#000000', 100)
        #RadioButton(self.all_sprites, 'rectangle.png', int(self.w * 0.65), int(self.h * 0.2), )
        pg.draw.rect(shared.screen, pg.Color('#000000'), (self.w * 0.65, self.h * 0.2, self.w * 0.022, self.h * 0.05),
                     1)

        Button(self.all_sprites, 'back.png', 0, 0, int(0.04 * self.w), int(0.04 * self.w), 'back')
        Button(self.all_sprites, 'leave_button.png', self.w * 0.958, 0, int(0.04 * self.w), int(0.04 * self.w), 'leave')

    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                raise KillEntireApp
            if event.type == pg.MOUSEBUTTONDOWN:
                for button in shared.all_buttons_cords:
                    if button.get_rect().collidepoint(event.pos):
                        if button.get_info() == 'back':
                            raise KillTopFrame
                        if button.get_info() == 'leave':
                            raise KillEntireApp
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    raise KillTopFrame
        self.draw_settings()
        self.all_sprites.draw(shared.screen)
        self.all_sprites.update()
        pg.display.flip()
