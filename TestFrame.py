from IFrame import IFrame
import shared
from Signals import *
import pygame as pg


class TestFrame1(IFrame):
    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                raise KillEntireApp()
        shared.screen.fill((125, 125, 0))
        pg.display.flip()


class TestFrame2(IFrame):
    def __init__(self):
        pg.display.set_caption('AAA')
    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                raise NewFrame(TestFrame1())
        shared.screen.fill((125, 125, 125))
        pg.display.flip()