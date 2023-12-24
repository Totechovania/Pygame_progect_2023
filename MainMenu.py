import pygame
import shared
import pygame as pg
import sys
import os
from IFrame import IFrame
from Signals import KillEntireApp
from FrameController import set_shared_variables


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pg.image.load(fullname)
    if colorkey is not None:
        pg.init()
        set_shared_variables()
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class MainMenu(IFrame):
    def __init__(self):
        pg.init()
        pg.display.set_caption('Game')
        set_shared_variables()
        self.main()
        self.main_button = True
        self.leave_button = True
        self.fight_button = True
        self.redactor_button = True
        self.campany_button = True
        self.settings_button = True
        self.back_button = False

    def update(self):
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                raise KillEntireApp
            if event.type == pg.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 1620 < x < 1800 and 620 < y < 850 and self.main_button:
                    self.main_button = False
                    self.leave_button = False
                    self.settings_button = False
                    self.back_button = True
                    self.fight_menu()
                if 3280 < x < 3440 and 0 < y < 150 and self.leave_button:
                    raise KillEntireApp
                if 0 < x < 150 and 0 < y < 150 and self.settings_button:
                    self.main_button = False
                    self.leave_button = False
                    self.settings_button = False
                    self.back_button = True
                    self.settings()
                if 0 < x < 150 and 0 < y < 150 and self.back_button:
                    self.main_button = True
                    self.leave_button = True
                    self.settings_button = True
                    self.back_button = False
                    self.main()

    def fight_menu(self):
        image = load_image('fon_menu.png')
        image = pygame.transform.scale(image, (shared.WIDTH, shared.HEIGHT))
        shared.screen.blit(image, (0, 0))

        font = pygame.font.Font(None, 200)
        text = font.render("Сражение", True, pg.Color('#00FF7F'))
        shared.screen.blit(text, (self.text_x - 150, self.text_y - 230))
        text_w = text.get_width()
        text_h = text.get_height()
        pygame.draw.rect(shared.screen, (0, 255, 0), (self.text_x - 150, self.text_y - 230,
                                                      text_w, text_h), 1)

        font = pygame.font.Font(None, 200)
        text = font.render("Редактор", True, pg.Color('#00FF7F'))
        shared.screen.blit(text, (self.text_x - 150, self.text_y + 100))
        text_h = text.get_height()
        pygame.draw.rect(shared.screen, (0, 255, 0), (self.text_x - 150, self.text_y + 100,
                                                      text_w, text_h), 1)

        font = pygame.font.Font(None, 200)
        text = font.render("Кампания", True, pg.Color('#00FF7F'))
        shared.screen.blit(text, (self.text_x - 150, self.text_y + 400))
        text_h = text.get_height()
        pygame.draw.rect(shared.screen, (0, 255, 0), (self.text_x - 150, self.text_y + 400,
                                                      text_w, text_h), 1)

        image_back = load_image('back.png')
        image_back = pygame.transform.scale(image_back, (150, 150))
        shared.screen.blit(image_back, (0, 0, 150, 150))

    def settings(self):
        image = load_image('fon_menu.png')
        image = pygame.transform.scale(image, (shared.WIDTH, shared.HEIGHT))
        shared.screen.blit(image, (0, 0))

        image_back = load_image('back.png')
        image_back = pygame.transform.scale(image_back, (150, 150))
        shared.screen.blit(image_back, (0, 0, 150, 150))

    def main(self):
        image = load_image('fon_menu.png')
        image = pygame.transform.scale(image, (shared.WIDTH, shared.HEIGHT))
        shared.screen.blit(image, (0, 0))
        font = pygame.font.Font(None, 100)
        text = font.render("MyAntiyoy", True, pg.Color('#00FF7F'))
        self.text_x = shared.WIDTH // 2 - text.get_width() // 2
        self.text_y = shared.HEIGHT // 2 - text.get_height() // 2 - 300
        shared.screen.blit(text, (self.text_x, self.text_y))
        pg.draw.polygon(shared.screen, pygame.Color('#30D5C8'),
                        [(self.text_x + 100, self.text_y + 270), (self.text_x + 250, self.text_y + 380),
                         (self.text_x + 100, self.text_y + 490)], 0)
        image_leave = load_image('leave_button.png')
        image_leave = pygame.transform.scale(image_leave, (150, 150))
        shared.screen.blit(image_leave, (shared.WIDTH - 150, 0))
        image_settings = load_image('settings_button.png')
        image_settings = pygame.transform.scale(image_settings, (150, 150))
        shared.screen.blit(image_settings, (0, 0, 150, 150))
