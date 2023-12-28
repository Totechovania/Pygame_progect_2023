from IFrame import IFrame
from Button import Button
from utilities import draw_fon
import pygame as pg
import shared
from Signals import KillEntireApp, KillTopFrame


class FightMenuWindow(IFrame):
    def __init__(self):
        self.w = shared.WIDTH
        self.h = shared.HEIGHT
        self.all_sprites = pg.sprite.Group()
        self.draw_fight_menu()

    def draw_fight_menu(self):
        draw_fon('fon_menu.png', self.w, self.h)

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

        self.draw_fight_menu()
        self.all_sprites.draw(shared.screen)
        self.all_sprites.update()
        pg.display.flip()
