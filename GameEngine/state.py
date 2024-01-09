from GameEngine.GameUnits.Buildings import *


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
