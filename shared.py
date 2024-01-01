# файл, который содержит переменные, используемые во всем проекте
# изменять только предназначенными для этого функциями

import pygame as pg

__all__ = (
    'WIDTH',
    'HEIGHT',
    'FPS',
    'screen',
    'clock',
)

FPS: int
WIDTH: int
HEIGHT: int
screen: pg.Surface
clock: pg.time.Clock
sound: bool
music: bool
