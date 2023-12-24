# файл, который содержит переменные, используемые во всем проекте
# изменять только преднозначенными для этого функциями

import pygame as pg

__all__ = (
    'WIDTH',
    'HEIGHT',
    'FPS',
    'display',
    'clock',
)

WIDTH: int
HEIGHT: int
display: pg.Surface
clock: pg.time.Clock
FPS: int
