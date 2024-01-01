import shared
from IFrame import IFrame
import pygame as pg
from Button import Button
from Signals import KillEntireApp


class ButtonDemonstration(IFrame):
    def __init__(self):
        self.buttons = pg.sprite.Group()
        exit_button = Button(self.buttons, 'leave_button.png')
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
