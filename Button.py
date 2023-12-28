import pygame as pg
import shared
from utilities import load_image


class Button(pg.sprite.Sprite):
    def __init__(self, group, filename, x, y, new_size_w=500, new_size_h=500, name=''):
        super().__init__(group)
        image = load_image(filename)
        image = pg.transform.scale(image, (new_size_w, new_size_h))
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = name
        shared.all_buttons_cords.append(self)

    def update(self, *args):
        pass

    def get_rect(self):
        return self.rect

    def get_info(self):
        return self.name
