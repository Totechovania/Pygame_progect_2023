# файл вспомогательных функций
import sys
import shared
import pygame as pg
import os
from PIL import Image, ImageFilter
from pyautogui import screenshot
from Signals import NewFrame, KillTopFrame, KillEntireApp
from math import cos, sin, pi
import json
import random


def terminate():
    pg.quit()
    sys.exit()


def apply_global_settings():
    pg.init()
    pg.display.set_caption('Game')


def set_shared_variables():
    info = pg.display.Info()
    w = info.current_w
    h = info.current_h
    if not os.path.exists('settings.json'):
        with open('settings.json', 'w') as f:
            json.dump(
                {"FULLSCREEN": True, "WIDTH": int(w * 0.581), "HEIGHT": int(h * 0.55), "SOUND": True, "MUSIC": True}, f)

    with open('settings.json', 'r') as f:
        f_data = json.load(f)
        shared.fullscreen = f_data['FULLSCREEN']
        shared.WIDTH = f_data['WIDTH']
        shared.HEIGHT = f_data['HEIGHT']
        shared.sound = f_data['SOUND']
        shared.music = f_data['MUSIC']
        try:
            if shared.fullscreen:
                shared.screen = pg.display.set_mode((info.current_w, info.current_h))
                shared.WIDTH = w
                shared.HEIGHT = h
            else:
                shared.screen = pg.display.set_mode((shared.WIDTH, shared.HEIGHT))
        except Exception:
            data = load_json_file()
            data['HEIGHT'] = int(h * 0.55)
            data['WIDTH'] = int(w * 0.581)
            change_json_file(data)
            shared.WIDTH = data['WIDTH']
            shared.HEIGHT = data['HEIGHT']
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
    info = pg.display.Info()
    w = info.current_w
    h = info.current_h
    data['SOUND'] = True
    data['MUSIC'] = True
    data['HEIGHT'] = int(h * 0.55)
    data['WIDTH'] = int(w * 0.581)
    data['FULLSCREEN'] = True
    change_json_file(data)
    raise KillEntireApp


def convert_image(filename):
    with Image.open('data/' + filename) as img:
        img.load()
        img = img.filter(ImageFilter.GaussianBlur(20))
        img.save('data/' + filename)


def open_pop_window():
    from Frames.PopUpWindow import PopUpWindow
    screenshot('data/screenshot.png')
    raise NewFrame(PopUpWindow())


def back():
    raise KillTopFrame


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


def blur_image(img, amt=10):
    raw_str = pg.image.tostring(img, 'RGBA', False)
    img = Image.frombytes('RGBA', img.get_size(), raw_str)
    img = img.filter(ImageFilter.GaussianBlur(amt))
    raw_str = img.tobytes('raw', 'RGBA')
    surf = pg.image.fromstring(raw_str, img.size, 'RGBA')
    return surf


def create_particles(position, groop, name):
    from Particles import Particle
    particle_count = 5
    numbers = [-6, -5, -4, -3, 3, 4, 5, 6]
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers), name, groop)


def get_size():
    data = load_json_file()
    return data['WIDTH'], data['HEIGHT']
