import shared
from IFrame import IFrame
from Signals import *
from utilities import terminate


class FrameController:
    def __init__(self, zero_frame: IFrame):
        self.frames = [zero_frame]

    def run(self):
        clock = shared.clock
        fps = shared.FPS

        while self.frames:
            clock.tick(fps)
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
