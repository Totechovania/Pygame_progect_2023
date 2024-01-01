import pygame as pg
import shared
from utilities import load_image


class Button(pg.sprite.Sprite):
    def __init__(self, group, image_path):
        super().__init__(group)
        self.func = None
        self.image = load_image(image_path)
        self.rect = self.image.get_rect()

    def connect(self, func: callable):
        self.func = func

    def update(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.func()



