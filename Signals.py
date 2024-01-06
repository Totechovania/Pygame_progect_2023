from Frames.IFrame import IFrame

__all__ = (
    'Signal',
    'NewFrame',
    'KillTopFrame',
    'KillEntireApp',
    'ApplySettings',
)


class Signal(Exception):
    pass


class NewFrame(Signal):
    def __init__(self, frame: IFrame):
        self.frame = frame


class KillTopFrame(Signal):
    pass


class KillEntireApp(Signal):
    pass


class ApplySettings(Signal):
    pass
