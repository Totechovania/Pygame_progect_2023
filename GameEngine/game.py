from GameEngine.GameUnits.Buildings import *
from GameEngine.GameUnits.Obstacles import *
from GameEngine.GameUnits.Units import *
from GameEngine.available_tiles import available_tiles
from GameEngine.state import State


class Game:
    def __init__(self, players, grid):
        self.players = players
        self.states = {}
        self.states_names = []
        self.grid = grid
        self.current_player = None
        self.current_player_id = -1
        self.generate_states()
        self.add_all_players()
        self.next_player()

    def add_player(self, state):
        self.states_names.append(state.owner)
        self.states[state.owner] = {'state': state, 'tiles': len(self.states[state.owner]), 'spent_money': 0,
                                    'earned_money': 0, 'captured_states': 0}

    def generate_states(self):
        for i in self.grid.grid:
            for j in i:
                if j.owner and j.owner not in self.states:
                    self.states[j.owner] = [j]
                elif j.owner:
                    self.states[j.owner].append(j)

    def add_all_players(self):
        for i in self.states:
            self.add_player(State(i, self.states[i]))
        self.states_names[self.states_names.index('Игрок')], self.states_names[0] = self.states_names[0], \
            self.states_names[self.states_names.index('Игрок')]

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

    def count_player_earnings(self):
        self.current_player.earnings = len(set(self.current_player.tiles)) + self.current_player.farms * 4
        self.current_player.tiles = list(set(self.current_player.tiles))
        for i in self.current_player.tiles:
            if isinstance(i.game_unit, Unit):
                self.current_player.earnings -= i.game_unit.pay

    def next_player(self):
        self.current_player_id = (self.current_player_id + 1) % self.players
        self.current_player = self.states[self.states_names[self.current_player_id]]['state']
        self.count_player_earnings()
        self.current_player.money += self.current_player.earnings
        if self.current_player.money < 0:
            for tile in self.current_player.tiles:
                if isinstance(tile.game_unit, Unit):
                    self.grid.unit = None
                    tile.set_game_unit(Grave(2))
                    self.current_player.money = 0
        self.count_player_earnings()
        self.current_player.set_turn()
        self.states[self.states_names[self.current_player_id - 1]]['state'].set_turn()

    def move(self, tile_from, tile_to):
        if self.available_move(tile_from) and isinstance(tile_from.game_unit, Unit):
            unit = tile_from.game_unit
            if tile_to in available_tiles(self.grid, tile_from, unit.power, unit.steps,
                                          tile_from.owner) and not tile_from.game_unit.moved:
                if isinstance(tile_to.game_unit, Guildhall):
                    self.remove_player(self.states[tile_to.owner]['state'])
                    self.states[tile_from.owner]['captured_states'] += 1
                tile_from.game_unit = None
                tile_to.owner = tile_from.owner
                tile_to.color = tile_from.color
                tile_to.set_game_unit(unit)
                tile_to.game_unit.moved = True
                self.states[tile_from.owner]['state'].new_tile(tile_to)
                self.count_player_earnings()
