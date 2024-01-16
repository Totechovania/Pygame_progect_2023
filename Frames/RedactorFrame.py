from Frames.IFrame import IFrame
import pygame as pg
from Signals import *
import shared
from GameEngine.HexGrid import HexGrid
from Frames.AbstractBaseFrame import AbstractBaseFrame
from utilities.Button import Button, ScrollWheelButton
from utilities.image import draw_text
from utilities.hexagons import hexagon_from_center
from GameEngine.GameUnits.Units import Peasant, Warrior, Knight, Spearman
from GameEngine.GameUnits.Obstacles import Tree, Grave, Rock
from GameEngine.GameUnits.Buildings import Guildhall, Farm, TowerFirst, TowerSecond

from GameEngine.Tile import HexTile


class RedactorFrame(AbstractBaseFrame):
    def __init__(self):
        super().__init__()
        self.bot_types = ['defender', 'attacker', 'farmer']
        self.w = shared.WIDTH
        self.h = shared.HEIGHT
        self.grid_rect = pg.Rect(0, round(self.w * 0.05), self.w, round(shared.HEIGHT * 0.8))

        self.grid_h = 10
        self.grid_w = 10

        self.grid = HexGrid.filled(self.grid_w, self.grid_h, 40, self.grid_rect)

        self.grid_is_moving = False

        self.chosen = None

        self.instrument = None
        self.chosen_button = None

        set_unit_instruments = {'guildhall', 'farm', 'towerfirst', 'towersecond', 'peasant', 'spearman', 'warrior', 'knight'}

        self.available_brush_parameters = [(None, (125, 125, 125)), (None, (255, 0, 0)), (None, (0, 255, 0)),] # todo add more owners and colors
        self.brush_par_index = 0

        self.builder_modes = [(125, 125, 125), (225, 225, 225)]
        self.builder_mode = 0 # 0 - tile, 1 - empty

        self.units_modes = [('peasant', 'peasant.png', Peasant),
                            ('spearman', 'spearman.png', Spearman),
                            ('warrior', 'warrior.png', Warrior),
                            ('knight', 'knight.png', Knight)]
        self.unit_mode = 0

        self.buildings_modes = [('farm', 'farm.png', Farm),
                                 ('towerfirst', 'towerfirst.png', TowerFirst),
                                 ('towersecond', 'towersecond.png', TowerSecond),
                                 ('guildhall', 'guildhall.png', Guildhall)]
        self.building_mode = 0

        self.obstacles_modes = [('tree', 'tree.png', Tree),
                                ('grave', 'grave32.png', Grave), #todo add grave.png
                                ('rock', 'rock.png', Rock)]
        self.obstacle_mode = 0

    def set_grid_size(self, w, h):
        self.grid_h = min(max(5, h), 60)
        self.grid_w = min(max(5, w), 60)

    def apply_grid_size(self):
        self.grid = HexGrid.filled(self.grid_w, self.grid_h, 40, self.grid_rect)

    def update(self):
        super().update()
        for event in self.events:
            if event.type == pg.MOUSEWHEEL:
                x, y = pg.mouse.get_pos()
                if self.grid.rect.collidepoint(x, y):
                    if event.y < 0:
                        self.grid.relative_scale(x, y, self.grid.scale * 0.9)
                    else:
                        self.grid.relative_scale(x, y, self.grid.scale * 1.1)
            if event.type == pg.MOUSEMOTION and pg.mouse.get_pressed()[1]:
                dx, dy = pg.mouse.get_rel()
                if self.grid_is_moving:
                    self.grid.move(dx, dy)
                else:
                    self.grid_is_moving = True
            else:
                self.grid_is_moving = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.grid.rect.collidepoint(event.pos):
                    chosen = self.grid.collide_point(*event.pos)
                    if chosen is not None:
                        self.use_instrument(chosen)

        self.buttons.update(self.events)
        pg.draw.rect(shared.screen, (255, 255, 255), self.grid_rect)


        self.grid.draw_tiles()

        x, y = pg.mouse.get_pos()
        if self.grid.rect.collidepoint(x, y):
            self.chosen = self.grid.collide_point(x, y)

        if self.chosen is not None:
            self.grid.draw_tile_stroke(self.chosen, (255, 255, 255), 4)

        self.grid.draw(shared.screen)
        pg.draw.rect(shared.screen, (0, 0, 0), self.grid_rect, round(self.h * 0.005))

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

        draw_text(f'w: {self.grid_w}', self.w * 0.653, self.w * 0.013, 'black', round(self.w * 0.032))
        draw_text(f'h: {self.grid_h}', self.w * 0.723, self.w * 0.013, 'black', round(self.w * 0.032))
        self.buttons.draw(shared.screen)

    def use_instrument(self, tile):
        if not isinstance(tile, HexTile):
            return
        if self.instrument == 'brush':
            owner, color = self.available_brush_parameters[self.brush_par_index]
            tile.set_owner(owner, color)
        elif self.instrument == 'builder':
            i, j = tile.indexes
            if self.builder_mode == 0:
                self.grid.set_tile(i, j)
            else:
                self.grid.set_empty(i, j)
        elif self.instrument == 'units':
            unit = self.units_modes[self.unit_mode][2](scale=2)
            tile.set_game_unit(unit)

        elif self.instrument == 'buildings':
            building = self.buildings_modes[self.building_mode][2](scale=2)
            tile.set_game_unit(building)
        elif self.instrument == 'obstacles':
            obstacle = self.obstacles_modes[self.obstacle_mode][2](scale=2)
            tile.set_game_unit(obstacle)

    def generate_buttons(self):
        super().generate_buttons()
        h = shared.HEIGHT * 0.90

        buildings_button = Button(
            (shared.WIDTH * 0.325, h, int(0.04 * self.w), int(0.04 * self.w)),
            'farm.png', self.buttons)
        buildings_button.connect(lambda: self.set_building(buildings_button))

        obstacles_button = Button(
            (shared.WIDTH * 0.225, h, int(0.04 * self.w), int(0.04 * self.w)),
            'tree.png', self.buttons)
        obstacles_button.connect(lambda: self.set_obstacle(obstacles_button))

        units_button = Button(
            (shared.WIDTH * 0.425, h, int(0.04 * self.w), int(0.04 * self.w)),
            'peasant.png', self.buttons)
        units_button.connect(lambda: self.set_unit(units_button))

        brush_button = Button(
            (shared.WIDTH * 0.125, h, int(0.04 * self.w), int(0.04 * self.w)),
            'brush.png', self.buttons)
        brush_button.connect(lambda: self.set_brush(brush_button))

        builder_button = Button(
            (shared.WIDTH * 0.025, h, int(0.04 * self.w), int(0.04 * self.w)),
            'builder.png', self.buttons)
        builder_button.connect(lambda: self.set_builder(builder_button))

        change_grid_width = ScrollWheelButton(
            (self.w * 0.65, self.w * 0.005, int(0.06 * self.w), int(0.04 * self.w)),
            'square.png', self.buttons
        )
        change_grid_width.connect_up(lambda: self.set_grid_size(self.grid_w + 1, self.grid_h))
        change_grid_width.connect_down(lambda: self.set_grid_size(self.grid_w - 1, self.grid_h))

        change_grid_height = ScrollWheelButton(
            (self.w * 0.72, self.w * 0.005, int(0.06 * self.w), int(0.04 * self.w)),
            'square.png', self.buttons
        )
        change_grid_height.connect_up(lambda: self.set_grid_size(self.grid_w, self.grid_h + 1))
        change_grid_height.connect_down(lambda: self.set_grid_size(self.grid_w, self.grid_h - 1))

        apply_grid_size_button = Button(
            (self.w * 0.8, self.w * 0.005, int(0.04 * self.w), int(0.04 * self.w)),
            'check.png', self.buttons
        )
        apply_grid_size_button.connect(self.apply_grid_size)


    def set_instrument(self, instrument, button):
        self.instrument = instrument
        self.chosen_button = button

    def set_unit(self, button):
        if self.instrument == 'units':
            self.unit_mode = (self.unit_mode + 1) % len(self.units_modes)
            button.set_image(self.units_modes[self.unit_mode][1])
        else:
            self.set_instrument('units', button)

    def set_building(self, button):
        if self.instrument == 'buildings':
            self.building_mode = (self.building_mode + 1) % len(self.buildings_modes)
            button.set_image(self.buildings_modes[self.building_mode][1])
        else:
            self.set_instrument('buildings', button)

    def set_obstacle(self, button):
        if self.instrument == 'obstacles':
            self.obstacle_mode = (self.obstacle_mode + 1) % len(self.obstacles_modes)
            button.set_image(self.obstacles_modes[self.obstacle_mode][1])
        else:
            self.set_instrument('obstacles', button)

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

