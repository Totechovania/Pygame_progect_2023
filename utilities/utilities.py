# файл вспомогательных функций
import sys
import shared
import pygame as pg
import os
from Signals import *
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
    if not os.path.exists('../settings.json'):
        with open('../settings.json', 'w') as f:
            json.dump(
                {"FULLSCREEN": True, "WIDTH": int(w * 0.581), "HEIGHT": int(h * 0.55), "SOUND": True, "MUSIC": True}, f)

    with open('../settings.json', 'r') as f:
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


def load_json_file():
    with open('../settings.json') as f:
        return json.load(f)


def change_json_file(data):
    with open('../settings.json', 'w') as f:
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


def create_particles(position, groop, name):
    from Particles import Particle
    particle_count = 5
    numbers = [-6, -5, -4, -3, 3, 4, 5, 6]
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers), name, groop)


def get_size():
    data = load_json_file()
    return data['WIDTH'], data['HEIGHT']
