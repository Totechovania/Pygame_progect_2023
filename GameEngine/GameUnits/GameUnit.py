import pygame as pg

from utilities.image import load_image


class GameUnit(pg.sprite.Sprite):
    images = {}

    def __init__(self, image_path: str, scale: float):
        super().__init__()
        if (image_path, scale) in self.images.keys():
            self.image = self.images[(image_path, scale)]
        else:
            self.image = load_image(image_path)
            self.image = pg.transform.scale_by(self.image, scale)
            self.images[(image_path, scale)] = self.image
        self.rect = self.image.get_rect()

    def adjust_to_tile(self, tile):
        self.rect.center = tile.center_x, tile.center_y

    def draw(self, surface: pg.Surface):
        surface.blit(pg.transform.scale(self.image, self.rect.size), self.rect)

    def to_string(self):
        raise NotImplemented

