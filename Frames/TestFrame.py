from IFrame import IFrame
import pygame as pg
from Signals import *
import shared


class TestFrame(IFrame):
    def __init__(self, parent: str = 'None'):
        self.font = pg.font.Font(None, 50)
        self.parent = parent

    def begin(self):
        print('begin')

    def end(self):
        print('end')

    def update(self):
        shared.screen.fill(pg.Color('black'))

        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                raise KillEntireApp

        text = self.font.render(f'Parent: {self.parent}', True, pg.Color('white'))
        shared.screen.blit(text, (0, 0))

        pg.display.flip()

    def pause(self):
        print('pause')

    def resume(self):
        print('resume')
