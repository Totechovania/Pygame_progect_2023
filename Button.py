import pygame as pg
import shared
from utilities import load_image


class Button(pg.sprite.Sprite):
    def __init__(self,
                 rect: tuple[int, int, int, int] | pg.Rect,
                 image_path: str,
                 *groups: pg.sprite.Group):
        super().__init__(*groups)
        self.func = None
        self.image = pg.transform.scale(load_image(image_path), (rect[2], rect[3]))
        self.rect = pg.Rect(rect)

    def connect(self, func: callable):
        self.func = func

    def update(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    if self.func is not None:
                        self.func()

    def draw(self, surface):
        surface.blit(self.image, self.rect)


