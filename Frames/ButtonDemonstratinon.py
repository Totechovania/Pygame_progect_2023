import shared
from IFrame import IFrame
import pygame as pg
from Button import Button
from Signals import KillEntireApp


class ButtonDemonstration(IFrame):
    def __init__(self):
        self.buttons = pg.sprite.Group()
        exit_rect = (0, 0, int(0.04 * shared.WIDTH), int(0.04 * shared.WIDTH))
        exit_button = Button(exit_rect, 'leave_button.png', self.buttons)
        exit_button.connect(self.exit)

    def exit(self):
        raise KillEntireApp

    def update(self):
        shared.screen.fill((255, 255, 255))

        events = pg.event.get()

        for event in events:
            if event.type == pg.QUIT:
                raise KillEntireApp

        self.buttons.update(events)
        self.buttons.draw(shared.screen)
