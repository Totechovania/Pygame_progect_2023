import os
import sys

from PIL import Image, ImageFilter
import pygame as pg

import shared


def blur_image(img, amt=10):
    raw_str = pg.image.tostring(img, 'RGBA', False)
    img = Image.frombytes('RGBA', img.get_size(), raw_str)
    img = img.filter(ImageFilter.GaussianBlur(amt))
    raw_str = img.tobytes('raw', 'RGBA')
    surf = pg.image.fromstring(raw_str, img.size, 'RGBA')
    return surf


def draw_text(text, x, y, color, size=50):
    font = pg.font.Font(None, size)
    to_print = font.render(text, True, pg.Color(color))
    shared.screen.blit(to_print, (x, y))


def load_image(name, colorkey=None):
    fullname = os.path.join('../data', name)
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
