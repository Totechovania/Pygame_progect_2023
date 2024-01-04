from IFrame import IFrame
import pygame as pg
from Signals import *
import shared
import time
from Frames.BlurTestFrame import BlurTestFrame


class TestFrame(IFrame):
    font_size = None
    font = None
    annotation_text = None
    history_text = None

    def __init__(self, previous: str = 'None', n=0, supposed_to_be: str = ''):
        if TestFrame.font_size is None:
            TestFrame.font_size = round(shared.HEIGHT / 20)
        if TestFrame.font is None:
            TestFrame.font = pg.font.Font(None, self.font_size)
        if TestFrame.annotation_text is None:
            TestFrame.annotation_text = self.font.render(f'Esc - kill top frame, N - new frame', True, pg.Color('white'))
        if TestFrame.history_text is None:
            TestFrame.history_text = self.font.render('History:', True, pg.Color('white'))

        self.supposed_to_be_text = self.font.render(supposed_to_be, True, pg.Color('white'))
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
                    self.draw_text()
                    raise NewFrame(BlurTestFrame(shared.screen.copy()))

        self.draw_text()

        pg.display.flip()

    def draw_text(self):
        previous_text = self.font.render(f'Previous: {self.previous}', True, pg.Color('white'))
        shared.screen.blit(previous_text, (0, 0))

        history_width = round(shared.WIDTH / 3)
        shared.screen.blit(self.history_text, (history_width, 0))
        for i, event in enumerate(self.history[-15:]):
            text = self.font.render(event, True, pg.Color('white'))
            shared.screen.blit(text, (history_width, self.font_size * (i + 1)))

        text = self.font.render(f'Supposed to be:', True, pg.Color('white'))
        shared.screen.blit(text, (round(shared.WIDTH * 3 / 5), 0))
        shared.screen.blit(self.supposed_to_be_text, (round(shared.WIDTH * 3 / 5), self.font_size))

        shared.screen.blit(self.annotation_text, (0, shared.HEIGHT - self.font_size))

    def pause(self):
        self.history.append(f'{time.strftime("%H:%M:%S")} - pause')

    def resume(self):
        self.history.append(f'{time.strftime("%H:%M:%S")} - resume')
