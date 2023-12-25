# файл вспомогательных функций
import sys
import shared
import pygame as pg


def terminate():
    pg.quit()
    sys.exit()


def apply_global_settings():
    pg.init()
    pg.display.set_caption('Game')


def set_shared_variables():
    display_info = pg.display.Info()
    shared.WIDTH = display_info.current_w
    shared.HEIGHT = display_info.current_h

    shared.screen = pg.display.set_mode((shared.WIDTH, shared.HEIGHT))

    shared.clock = pg.time.Clock()
    shared.FPS = 60
