from GameEngine.GameUnits.Units import *


class State:
    def __init__(self, owner, player):
        self.owner = owner
        self.tiles = []
        self.money = 20
        self.earnings = 10
        self.turn = False
        self.player = player

    def new_tile(self, tile):
        self.tiles.append(tile)

    def lose_tile(self, tile):
        if isinstance(tile.game_unit, Farm):
            self.earnings -= 6
        del self.tiles[(self.tiles.index(tile))]

    def set_turn(self):
        if self.turn:
            self.turn = False
        else:
            self.turn = True
