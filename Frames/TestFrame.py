from IFrame import IFrame
import pygame as pg
from Signals import *
import shared
import time


class TestFrame(IFrame):
    font = None
    annotation_text = None
    history_text = None

    def __init__(self, previous: str = 'TestFrame', n=0):
        if TestFrame.font is None:
            TestFrame.font = pg.font.Font(None, 50)
        if TestFrame.annotation_text is None:
            TestFrame.annotation_text = self.font.render(f'Esc - kill top frame, N - new frame', True, pg.Color('white'))
        if TestFrame.history_text is None:
            TestFrame.history_text = self.font.render('History:', True, pg.Color('white'))

        self.n = n
        self.previous = previous
        self.history = []

    def begin(self):
        self.history.append(f'{time.strftime("%H:%M:%S")} - begin')

    def end(self):
        self.history.append(f'{time.strftime("%H:%M:%S")} - end')

    def update(self):
        shared.screen.fill(pg.Color('black'))

        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                raise KillEntireApp
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    raise KillTopFrame
                if event.key == pg.K_n:
                    raise NewFrame(TestFrame(n=self.n + 1))

        previous_text = self.font.render(f'Previous: {self.previous}{self.n}', True, pg.Color('white'))
        shared.screen.blit(previous_text, (0, 0))

        shared.screen.blit(self.history_text, (500, 0))
        for i, event in enumerate(self.history):
            text = self.font.render(event, True, pg.Color('white'))
            shared.screen.blit(text, (500, 50 * (i + 1)))

        shared.screen.blit(self.annotation_text, (0, shared.HEIGHT - 100))

        pg.display.flip()

    def pause(self):
        self.history.append(f'{time.strftime("%H:%M:%S")} - pause')

    def resume(self):
        self.history.append(f'{time.strftime("%H:%M:%S")} - resume')
