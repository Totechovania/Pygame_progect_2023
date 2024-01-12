from GameEngine.GameUnits.Units import *
from GameEngine.GameUnits.Buildings import *
from GameEngine.GameUnits.Obstacles import *
from GameEngine.available_tiles import available_tiles
from GameEngine.tile_defense import tile_defense
from random import choice


class Bot:
    def __init__(self):
        self.steps = 0
        self.state = None
        self.game = None

    def do_move(self):
        if self.steps < 10:
            self.explorer()
        if self.steps == 3 or self.steps == 4:
            self.defender()
        else:
            self.defender()
        self.forgotten_units_to_move()
        self.steps += 1

    def explorer(self):
        for i in range(self.state.money // 4 // 10):
            tiles = list(filter(lambda x: not x.game_unit or isinstance(x.game_unit, Tree), self.state.tiles))
            if tiles and self.state.earnings - 1 > 0:
                self.game.new_unit(choice(tiles), Peasant(2))
        tiles = list(filter(lambda x: isinstance(x.game_unit, Peasant) and not x.game_unit.moved, self.state.tiles))
        for el in tiles:
            available_to_move_tiles = list(
                filter(lambda x: not x.owner or isinstance(x.game_unit, Tree), available_tiles(self.game.grid,
                                                                                               el,
                                                                                               el.game_unit.power,
                                                                                               el.game_unit.steps,
                                                                                               el.owner)))
            if available_to_move_tiles:
                self.game.move(el, choice(available_to_move_tiles))

    def farmer(self):
        tiles = []
        for el in list(filter(lambda x: isinstance(x.game_unit, (Guildhall, Farm)), self.state.tiles)):
            for el_2 in self.game.grid.get_adjacent_tiles(el):
                tiles.append(el_2)
        for i in range(self.state.money // 2 // (12 + self.state.farms * 4)):
            if (self.state.money // 2 - (12 + self.state.farms * 4)) > 0 and tiles:
                self.game.new_unit(choice(tiles), Farm(2))
            else:
                break

    def defender(self):
        for i in range(self.state.money // 2 // 15):
            tiles = list(filter(lambda x: not x.game_unit and tile_defense(self.game.grid, x) < 3, self.state.tiles))
            if not tiles:
                break
            tile = choice(tiles)
            if self.state.money > 120:
                self.game.new_unit(tile, TowerSecond(2))
            elif self.state.money // 2 - 15 and tile_defense(self.game.grid, tile) < 2:
                self.game.new_unit(tile, TowerFirst(2))
            else:
                break

    def forgotten_units_to_move(self):
        tiles = list(filter(lambda x: isinstance(x.game_unit, Unit) and not x.game_unit.moved, self.state.tiles))
        for el in tiles:
            available_to_move_tiles = available_tiles(self.game.grid, el, el.game_unit.power, el.game_unit.steps,
                                                      el.owner)
            for tile in filter(lambda x: x.owner != self.game.current_player.owner, available_to_move_tiles):
                if isinstance(el.game_unit, Peasant):
                    if not tile.owner:
                        self.game.move(el, tile)
                        break
                else:
                    if tile.owner:
                        self.game.move(el, tile)
                        break
            if available_to_move_tiles:
                self.game.move(el, choice(available_to_move_tiles))
