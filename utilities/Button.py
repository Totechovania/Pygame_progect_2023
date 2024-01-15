import pygame as pg
from utilities.image import load_image
from utilities.music import play_sound


class Button(pg.sprite.Sprite):
    def __init__(self, rect: tuple or list or pg.Rect, image_path: str, *groups: pg.sprite.Group,
                 change_under_mouse: bool = True):
        super().__init__(*groups)
        self.func = None
        self.image = pg.transform.scale(load_image(image_path), (rect[2], rect[3]))
        self.rect = pg.Rect(rect)

        self.main_image = self.image
        self.main_rect = self.rect

        self.change_under_mouse = change_under_mouse
        self.under_mouse_rect = pg.Rect(rect[0], rect[1], rect[2] * 1.2, rect[3] * 1.2)
        self.under_mouse_rect.center = self.rect.center
        self.under_mouse_image = pg.transform.scale(load_image(image_path), (rect[2] * 1.2, rect[3] * 1.2))

    def connect(self, func: callable):
        self.func = func

    def update(self, events):
        if events is not None:
            for event in events:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.rect.collidepoint(event.pos):
                            if self.func is not None:
                                play_sound('button_press.mp3')
                                self.func()
        if self.change_under_mouse and self.rect.collidepoint(pg.mouse.get_pos()):
            self.image = self.under_mouse_image
            self.rect = self.under_mouse_rect
        else:
            self.image = self.main_image
            self.rect = self.main_rect

    def set_image(self, image_path: str):
        self.main_image = pg.transform.scale(load_image(image_path), (self.main_rect[2], self.main_rect[3]))
        self.under_mouse_image = pg.transform.scale(load_image(image_path), (self.main_rect[2] * 1.2, self.main_rect[3] * 1.2))
