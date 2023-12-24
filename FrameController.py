import pygame as pg

import shared
from IFrame import IFrame
from Signals import *
from utilities import terminate


class FrameController:
    def __init__(self, zero_frame: IFrame):
        self.frames = [zero_frame]

    def run(self):
        apply_global_settings()
        set_shared_variables()

        clock = shared.clock

        while self.frames:
            clock.tick(shared.FPS)
            try:
                self.frames[-1].update()
            except Signal as e:
                self.handle_signal(e)

    def handle_signal(self, signal: Signal):
        if isinstance(signal, NewFrame):
            self.handle_new_frame(signal.frame)
        elif isinstance(signal, KillTopFrame):
            self.handle_kill_top_frame()
        elif isinstance(signal, KillEntireApp):
            self.handle_kill_entire_app()

    def handle_new_frame(self, frame: IFrame):
        self.frames[-1].pause()
        self.frames.append(frame)
        self.frames[-1].begin()

    def handle_kill_top_frame(self):
        self.frames[-1].end()
        self.frames.pop()
        if self.frames:
            self.frames[-1].resume()

    def handle_kill_entire_app(self):
        for frame in self.frames:
            frame.end()
        terminate()


def apply_global_settings():
    pg.init()
    pg.display.set_caption('Game')


def set_shared_variables():
    display_info = pg.display.Info()
    shared.WIDTH = display_info.current_w
    shared.HEIGHT = display_info.current_h

    shared.sceen = pg.display.set_mode((shared.WIDTH, shared.HEIGHT))

    shared.clock = pg.time.Clock()
    shared.FPS = 60
