from IFrame import IFrame
from Button import Button
from utilities import draw_fon, draw_text
import pygame as pg
import shared
from Signals import KillEntireApp, KillTopFrame, NewFrame
from Frames.FightMenuWindow import FightMenuWindow
from Frames.Download import Download
from Frames.Campany import Campany
from Frames.Redactor import Redactor


class ChooseMode(IFrame):
    def __init__(self):
        self.w = shared.WIDTH
        self.h = shared.HEIGHT
        self.all_sprites = pg.sprite.Group()
        self.draw_choose_mode()

    def draw_choose_mode(self):
        draw_fon('fon_menu.png', self.w, self.h)

        Button(self.all_sprites, 'back.png', 0, 0, int(0.04 * self.w), int(0.04 * self.w), 'back')
        Button(self.all_sprites, 'leave_button.png', self.w * 0.958, 0, int(0.04 * self.w), int(0.04 * self.w), 'leave')
        Button(self.all_sprites, 'rectangle.png', self.w * 0.4, self.h * 0.1, int(self.w * 0.2), int(self.w * 0.08),
               'fight')
        Button(self.all_sprites, 'rectangle.png', self.w * 0.4, self.h * 0.25, int(self.w * 0.2), int(self.w * 0.08),
               'redactor')
        Button(self.all_sprites, 'rectangle.png', self.w * 0.4, self.h * 0.4, int(self.w * 0.2), int(self.w * 0.08),
               'campany')
        Button(self.all_sprites, 'rectangle.png', self.w * 0.4, self.h * 0.55, int(self.w * 0.2), int(self.w * 0.08),
               'download')

        draw_text('Сражение', self.w // 2.35, self.h // 6.3, '#08E8DE', int(self.w * 0.045))
        draw_text('Редактор', self.w // 2.35, self.h // 3.25, '#08E8DE', int(self.w * 0.045))
        draw_text('Кампания', self.w // 2.35, self.h // 2.15, '#08E8DE', int(self.w * 0.045))
        draw_text('Загрузить', self.w // 2.35, self.h // 1.62, '#08E8DE', int(self.w * 0.045))

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
                        if button.get_info() == 'fight':
                            raise NewFrame(FightMenuWindow())
                        if button.get_info() == 'redactor':
                            raise NewFrame(Redactor())
                        if button.get_info() == 'campany':
                            raise NewFrame(Campany())
                        if button.get_info() == 'download':
                            raise NewFrame(Download())
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    raise KillTopFrame
        self.draw_choose_mode()
        self.all_sprites.draw(shared.screen)
        self.all_sprites.update()
        pg.display.flip()
