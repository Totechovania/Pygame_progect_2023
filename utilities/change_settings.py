# файл вспомогательных функций
import shared
import pygame as pg
import os
import json


def set_shared_variables():
    info = pg.display.Info()
    shared.fullscreen_w = info.current_w
    shared.fullscreen_h = info.current_h
    if not os.path.exists('settings.json'):
        with open('settings.json', 'w') as f:
            json.dump(
                {"FULLSCREEN": True, "WIDTH": int(shared.fullscreen_w * 0.581),
                 "HEIGHT": int(shared.fullscreen_h * 0.55), "SOUND": True, "MUSIC": True}, f)

    with open('settings.json', 'r') as f:
        f_data = json.load(f)
        shared.fullscreen = f_data['FULLSCREEN']
        shared.WIDTH = f_data['WIDTH']
        shared.HEIGHT = f_data['HEIGHT']
        shared.sound = f_data['SOUND']
        shared.music = f_data['MUSIC']
        if not (500 < shared.WIDTH < shared.fullscreen_w):
            shared.WIDTH = int(shared.fullscreen_w * 0.55)
        if not (300 < shared.HEIGHT < shared.fullscreen_h):
            shared.HEIGHT = int(shared.fullscreen_h * 0.581)
        if shared.fullscreen:
            shared.screen = pg.display.set_mode((shared.fullscreen_w, shared.fullscreen_h))
            shared.WIDTH = shared.fullscreen_w
            shared.HEIGHT = shared.fullscreen_h
        if not shared.fullscreen:
            shared.screen = pg.display.set_mode((shared.WIDTH, shared.HEIGHT))
        shared.clock = pg.time.Clock()
        shared.FPS = 60


def load_json_file():
    with open('settings.json') as f:
        return json.load(f)


def change_json_file(data):
    with open('settings.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_size():
    data = load_json_file()
    return data['WIDTH'], data['HEIGHT']
