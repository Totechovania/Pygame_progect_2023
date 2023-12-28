# файл вспомогательных функций
import sys
import shared
import pygame as pg
import os


def terminate():
    pg.quit()
    sys.exit()


def apply_global_settings():
    pg.init()
    pg.display.set_caption('Game')


def set_shared_variables():
    display_info = pg.display.Info()
    shared.WIDTH = round(display_info.current_w * 0.8)
    shared.HEIGHT = round(display_info.current_h * 0.8)

    shared.screen = pg.display.set_mode((shared.WIDTH, shared.HEIGHT))

    shared.clock = pg.time.Clock()
    shared.FPS = 60


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pg.image.load(fullname)
    if colorkey is not None:
        pg.init()
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image
