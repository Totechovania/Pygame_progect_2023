from GameEngine.GameUnits.Buildings import *
from GameEngine.GameUnits.Obstacles import *
from GameEngine.GameUnits.Units import *
from GameEngine.available_tiles import available_tiles


class Game:
    def __init__(self, players):
        self.players = players
        self.states = {}
        self.states_names = []
        self.grid = None
        self.current_player = None
        self.current_player_id = -1

    def add_player(self, state):
        self.states_names.append(state.owner)
        self.states[state.owner] = {'state': state, 'tiles': 0, 'money': 0, 'captured_states': 0}

    def remove_player(self, state):
        del self.states[state.owner]
        del self.states_names[self.states_names.index(state.owner)]
        self.players -= 1
        if self.players == 1:
            return self.states['state']
        return None

    def available_move(self, tile):
        if tile.owner == self.current_player.owner:
            return True
        return False

    def next_player(self):
        self.current_player_id = (self.current_player_id + 1) % self.players
        self.current_player = self.states[self.states_names[self.current_player_id]]['state']
        self.current_player.money += self.current_player.earnings
        if self.current_player.money < 0:
            for tile in self.current_player.tiles:
                if tile.game_unit:
                    self.grid[tile.indexes].set_tile()
                    tile.set_game_unit(Grave(2))
        self.current_player.set_turn()

    def move(self, tile_from, tile_to):
        if self.available_move(tile_from):
            unit = tile_from.game_unit
            if tile_to in available_tiles(self.grid, tile_from, unit.power, unit.step, tile_from.owner):
                self.grid[tile_from.indexes].set_tile()
                if isinstance(tile_to.game_unit, Guildhall):
                    self.remove_player(self.states[tile_to.owner]['state'])
                tile_to.set_game_unit(unit)
                tile_to.owner = tile_from.owner
                self.states[tile_from.owner]['state'].add_tile(tile_to)
