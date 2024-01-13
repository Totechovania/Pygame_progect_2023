from GameEngine.GameUnits.Buildings import *
from GameEngine.GameUnits.Obstacles import Grave
from GameEngine.GameUnits.Units import Unit


class State:
    def __init__(self, owner, tiles, bot):
        self.owner = owner
        self.tiles = tiles
        self.money = 20
        self.farms = 0
        self.earnings = 10
        self.bot = bot
        self.turn = False

    def new_tile(self, tile):
        self.tiles.append(tile)

    def lose_tile(self, tile):
        if isinstance(tile.game_unit, Farm):
            self.farms -= 1
        del self.tiles[self.tiles.index(tile)]

    def set_turn(self):
        if self.turn:
            self.turn = False
        else:
            self.turn = True

    def lose_game_state(self):
        for el in filter(lambda x: x.game_unit and isinstance(x.game_unit, Unit), self.tiles):
            el.set_game_unit(Grave('grave32.png'))
