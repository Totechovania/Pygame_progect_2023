import pygame as pg
import shared
import os


def play_sound(sound_name: str) -> None:
    if shared.sound:
        sound = pg.mixer.Sound(os.path.join("data/", sound_name))
        sound.play(loops=0)


def play_background_music(music_name: str) -> None:
    if shared.music:
        pg.mixer.music.load(os.path.join("data/", music_name))
        pg.mixer.music.play(loops=-1)
    else:
        pg.mixer.music.stop()
