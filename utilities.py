# файл вспомогательных функций
import sys
import shared
import pygame as pg
import os
from PIL import Image, ImageFilter
from Signals import NewFrame, KillTopFrame, KillEntireApp
from math import cos, sin, pi
import json


def terminate():
    pg.quit()
    sys.exit()


def apply_global_settings():
    pg.init()
    pg.display.set_caption('Game')


def set_shared_variables():
    with open('settings.json', 'r') as f:
        f_data = json.load(f)
        shared.fullscreen = f_data['FULLSCREEN']
        shared.WIDTH = f_data['WIDTH']
        shared.HEIGHT = f_data['HEIGHT']
        shared.sound = f_data['SOUND']
        shared.music = f_data['MUSIC']
        if shared.fullscreen:
            shared.screen = pg.display.set_mode((shared.WIDTH, shared.HEIGHT), pg.FULLSCREEN)
        else:
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


def draw_text(text, x, y, color, size=50):
    font = pg.font.Font(None, size)
    to_print = font.render(text, True, pg.Color(color))
    shared.screen.blit(to_print, (x, y))


def load_json_file():
    with open('settings.json') as f:
        return json.load(f)


def change_json_file(data):
    with open('settings.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def set_default_settings():
    data = load_json_file()
    data['SOUND'] = True
    data['MUSIC'] = True
    data['HEIGHT'] = 800
    data['WIDTH'] = 2000
    data['FULLSCREEN'] = True
    change_json_file(data)
    raise KillEntireApp


def blur_image(img, amt=10):
    raw_str = pg.image.tostring(img, 'RGBA', False)
    img = Image.frombytes('RGBA', img.get_size(), raw_str)
    img = img.filter(ImageFilter.GaussianBlur(amt))
    raw_str = img.tobytes('raw', 'RGBA')
    surf = pg.image.fromstring(raw_str, img.size, 'RGBA')
    return surf


def hexagon_from_center(center_x: float, center_y: float, radius: float) -> list[tuple[int, int]]:
    vertices = []
    start_x = 0
    start_y = radius
    for i in range(6):
        angle = pi / 3 * i
        x = start_x * cos(angle) - start_y * sin(angle)
        y = start_x * sin(angle) + start_y * cos(angle)
        vertices.append((round(x + center_x),
                         round(y + center_y)))

    return vertices
