import pygame as pg
from utilities.image import load_image
import shared


class GameUnit(pg.sprite.Sprite):
    images = {}
    counter = 0

    def __init__(self, image_path: str, scale: float, columns=1, rows=1):
        super().__init__(shared.animated_units)

        if '32' in image_path:
            columns = 1

        self.image_path = image_path
        self.scale = scale
        self.frames = []
        self.cur_frame = 0
        self.stop = False

        if (image_path, scale) in self.images.keys():
            self.image = self.images[(image_path, scale)][self.cur_frame]
        else:
            self.image = load_image(image_path)
            self.image = pg.transform.scale_by(self.image, scale)
            self.cut_sheet(self.image, columns, rows)
            self.image = self.frames[self.cur_frame]
            self.images[(image_path, scale)] = self.frames
        self.rect = self.image.get_rect()

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pg.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pg.Rect(frame_location, self.rect.size)))

    def adjust_to_tile(self, tile):
        self.rect.center = tile.center_x, tile.center_y

    def draw(self, surface: pg.Surface):
        surface.blit(pg.transform.scale(self.image, self.rect.size), self.rect)

    def update(self):
        if self.counter % 8 == 0:
            if not self.stop:
                self.cur_frame = (self.cur_frame + 1) % len(self.images[(self.image_path, self.scale)])
            self.image = self.images[(self.image_path, self.scale)][self.cur_frame]
        self.counter += 1
