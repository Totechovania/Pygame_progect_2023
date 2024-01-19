import sys
import pygame as pg


def terminate():
    pg.quit()
    sys.exit()


def apply_global_settings():
    pg.init()
    pg.display.set_caption('Game')
