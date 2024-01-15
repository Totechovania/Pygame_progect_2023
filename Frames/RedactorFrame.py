from Frames.IFrame import IFrame
import pygame as pg
from Signals import *
import shared
from GameEngine.HexGrid import HexGrid
from Frames.AbstractBaseFrame import AbstractBaseFrame
from utilities.Button import Button
from utilities.image import load_image
from utilities.hexagons import hexagon_from_center


class RedactorFrame(AbstractBaseFrame):
    def __init__(self):
        super().__init__()
        self.bot_types = ['defender', 'attacker', 'farmer']
        self.w = shared.WIDTH
        self.h = shared.HEIGHT
        self.grid_rect = pg.Rect(0, round(self.w * 0.05), self.w, round(shared.HEIGHT * 0.8))

        self.grid = HexGrid.filled(10, 10, 40, self.grid_rect)

        self.grid_is_moving = False

        self.chosen = None

        self.instrument = None
        self.chosen_button = None

        instruments = ['farm', 'towerfirst', 'towersecond', 'peasant', 'spearman', 'warrior', 'knight']

        self.available_brush_parameters = [(None, (125, 125, 125)), (None, (255, 0, 0)), (None, (0, 255, 0)),]
        self.brush_par_index = 0

        self.builder_modes = [(125, 125, 125), (225, 225, 225)]
        self.builder_mode = 0 # 0 - tile, 1 - empty

    def update(self):
        super().update()
        for event in self.events:
            if event.type == pg.MOUSEWHEEL:
                x, y = pg.mouse.get_pos()
                if event.y < 0:
                    self.grid.relative_scale(x, y, self.grid.scale * 0.9)
                else:
                    self.grid.relative_scale(x, y, self.grid.scale * 1.1)
            elif event.type == pg.MOUSEMOTION and pg.mouse.get_pressed()[1]:
                dx, dy = pg.mouse.get_rel()
                if self.grid_is_moving:
                    self.grid.move(dx, dy)
                else:
                    self.grid_is_moving = True
            else:
                self.grid_is_moving = False

        self.buttons.update(self.events)
        pg.draw.rect(shared.screen, (255, 255, 255), self.grid_rect)

        self.grid.draw_tiles()

        x, y = pg.mouse.get_pos()
        if self.grid.rect.collidepoint(x, y):
            self.chosen = self.grid.collide_point(x, y)

        if self.chosen is not None:
            self.grid.draw_tile_stroke(self.chosen, (255, 255, 255), 4)

        self.grid.draw(shared.screen)

        if self.chosen_button is not None:
            x, y = self.chosen_button.rect.center
            rad = self.chosen_button.rect.height / 2 + round(self.w * 0.01)

            if self.instrument == 'brush':
                color = self.available_brush_parameters[self.brush_par_index][1]
            elif self.instrument == 'builder':
                color = self.builder_modes[self.builder_mode]
            else:
                color = (125, 125, 125)

            hexagon = hexagon_from_center(x, y, rad)
            pg.draw.polygon(shared.screen, color, hexagon)
            pg.draw.polygon(shared.screen, (0, 0, 0), hexagon, round(self.w * 0.003))

        self.buttons.draw(shared.screen)

    def generate_buttons(self):
        super().generate_buttons()
        h = shared.HEIGHT * 0.90
        guildhall_button = Button((shared.WIDTH * 0.025, h, int(0.04 * self.w), int(0.04 * self.w)),
                                  'guildhall.png', self.buttons)
        guildhall_button.connect(lambda: self.set_instrument('guildhall', guildhall_button))

        farmhouse_button = Button((shared.WIDTH * 0.125, h, int(0.04 * self.w), int(0.04 * self.w)),
                                  'farm.png', self.buttons)
        farmhouse_button.connect(lambda: self.set_instrument('farm', farmhouse_button))

        tower_level_1 = Button((shared.WIDTH * 0.225, h, int(0.04 * self.w), int(0.04 * self.w)),
                               'towerfirst.png', self.buttons)
        tower_level_1.connect(lambda: self.set_instrument('towerfirst', tower_level_1))

        tower_level_2 = Button((shared.WIDTH * 0.325, h, int(0.04 * self.w), int(0.04 * self.w)),
                               'towersecond.png', self.buttons)
        tower_level_2.connect(lambda: self.set_instrument('towersecond', tower_level_2))

        traveller_summon_button = Button(
            (shared.WIDTH * 0.625, h, int(0.04 * self.w), int(0.04 * self.w)),
            'peasant.png', self.buttons)
        traveller_summon_button.connect(lambda: self.set_instrument('peasant', traveller_summon_button))

        spearman_summon_button = Button(
            (shared.WIDTH * 0.725, h, int(0.04 * self.w), int(0.04 * self.w)),
            'spearman.png', self.buttons)
        spearman_summon_button.connect(lambda: self.set_instrument('spearman', spearman_summon_button))

        warrior_summon_button = Button(
            (shared.WIDTH * 0.825, h, int(0.04 * self.w), int(0.04 * self.w)),
            'warrior.png', self.buttons)
        warrior_summon_button.connect(lambda: self.set_instrument('warrior', warrior_summon_button))

        knight_summon_button = Button(
            (shared.WIDTH * 0.925, h, int(0.04 * self.w), int(0.04 * self.w)),
            'knight.png', self.buttons)
        knight_summon_button.connect(lambda: self.set_instrument('knight', knight_summon_button))

        brush_button = Button(
            (shared.WIDTH * 0.525, h, int(0.04 * self.w), int(0.04 * self.w)),
            'brush.png', self.buttons)
        brush_button.connect(lambda: self.set_brush(brush_button))

        builder_button = Button(
            (shared.WIDTH * 0.425, h, int(0.04 * self.w), int(0.04 * self.w)),
            'builder.png', self.buttons)
        builder_button.connect(lambda: self.set_builder(builder_button))

    def set_instrument(self, instrument, button):
        self.instrument = instrument
        self.chosen_button = button

    def set_brush(self, button):
        if self.instrument == 'brush':
            self.brush_par_index = (self.brush_par_index + 1) % len(self.available_brush_parameters)
        else:
            self.set_instrument('brush', button)

    def set_builder(self, button):
        if self.instrument == 'builder':
            self.builder_mode = (self.builder_mode + 1) % len(self.builder_modes)
        else:
            self.set_instrument('builder', button)

