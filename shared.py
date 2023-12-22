# файл, который содержит переменные, используемые во всем проекте
# изменять только преднозначенными для этого функциями

import pygame

__all__ = (
    'WIDTH',
    'HEIGHT',
    'FPS',
    'display',
    'clock',
)

FPS: int
WIDTH: int
HEIGHT: int
display: pygame.Surface
clock: pygame.time.Clock

