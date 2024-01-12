from GameEngine.GameUnits.Units import *
from GameEngine.available_tiles import available_tiles
from random import choice


class Bot:
    def __init__(self):
        self.state = None
        self.game = None

    def do_move(self):
        self.explorer()

    def explorer(self):
        for i in range(self.state.money // 10):
            tiles = list(filter(lambda x: not x.game_unit, self.state.tiles))
            if tiles and self.state.earnings - 1 > 0:
                self.game.new_unit(choice(tiles), Peasant(2))
        tiles = list(filter(lambda x: isinstance(x.game_unit, Peasant) and not x.game_unit.moved, self.state.tiles))
        for el in tiles:
            available_to_move_tiles = list(filter(lambda x: not x.owner, available_tiles(self.game.grid,
                                                                                         el, el.game_unit.power,
                                                                                         el.game_unit.steps, el.owner)))
            if available_to_move_tiles:
                self.game.move(el, choice(available_to_move_tiles))
