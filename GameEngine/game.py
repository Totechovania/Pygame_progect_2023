from GameEngine.GameUnits.Buildings import *
from GameEngine.GameUnits.Obstacles import *
from GameEngine.GameUnits.Units import *
from GameEngine.Tile import EmptyTile
from GameEngine.available_tiles import available_tiles
from GameEngine.tile_defense import tile_defense
from GameEngine.state import State
from GameEngine.Bot import Bot


class Game:

    def __init__(self, players, grid):
        self.players = players
        self.states = {}
        self.operational_list = []
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
        try:
            for i in self.states:
                bot = Bot()
                self.add_player(State(i, self.states[i], bot))
                bot.state = self.states[i]['state']
                bot.game = self
                #print(self.states[i]['state'])
            self.states_names[self.states_names.index('Игрок')], self.states_names[0] = self.states_names[0], \
                self.states_names[self.states_names.index('Игрок')]
        except Exception:
            pass

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
        #print(self.players, self.current_player_id, self.current_player, self.states, self.states_names)
        self.current_player_id = (self.current_player_id + 1) % self.players
        self.current_player = self.states[self.states_names[self.current_player_id]]['state']
        self.count_player_earnings()
        self.current_player.money += self.current_player.earnings
        if 'Игрок' in self.states_names:
            self.states[self.current_player.owner]['earned_money'] += self.states['Игрок']['state'].earnings
        for i in self.current_player.tiles:
            if isinstance(i.game_unit, Unit):
                i.game_unit.moved = False
        if self.current_player.money < 0:
            for tile in self.current_player.tiles:
                if isinstance(tile.game_unit, Unit):
                    self.grid.unit = None
                    tile.set_game_unit(Grave(2))
                    self.current_player.money = 0
        self.count_player_earnings()
        self.current_player.set_turn()
        self.states[self.states_names[self.current_player_id - 1]]['state'].set_turn()
        if self.current_player.owner != 'Игрок':
            self.current_player.bot.do_move()
            self.next_player()
        self.operational_list.clear()

    def check_defense(self, tile, unit):
        if tile.owner is None and (not isinstance(tile.game_unit, Rock) or tile.game_unit is None):
            return True
        elif tile.game_unit and not tile.game_unit.power < unit.power:
            return False
        indexes = tile.indexes
        if tile.owner == self.current_player.owner:
            return True
        if tile_defense(self.grid, tile) >= unit.power:
            return False
        for tile in self.grid.get_adjacent_tiles((indexes[0], indexes[1])):
            if tile.game_unit:
                if tile.game_unit.power > unit.power:
                    if tile.owner != self.current_player.owner and not isinstance(tile.game_unit, Rock):
                        return False
        return True

    def check_near(self, check_tile):
        indexes = check_tile.indexes
        for tile in self.grid.get_adjacent_tiles((indexes[0], indexes[1])):
            if tile.owner == self.current_player.owner:
                return True

    # def back_move(self):
    #     print('Работает')
    #     try:
    #         grid, self.states = self.operational_list.pop(-1)
    #         if grid == self.grid.grid:
    #             print(self.grid)
    #         return self.grid
    #     except IndexError:
    #         print(self.operational_list)
    #         return self.grid

    def new_unit(self, tile, unit):
        if isinstance(tile, EmptyTile):
            return False
        if (self.available_move(tile) or self.check_near(tile)) and (
                not isinstance(unit, Building) or tile.owner == 'Игрок') and \
                self.check_defense(tile, unit) and unit.cost <= self.current_player.money and \
                not isinstance(tile, EmptyTile):
            if isinstance(unit, Farm) and unit.cost + (self.current_player.farms * 4) > self.current_player.money:
                return False

            if isinstance(tile.game_unit, Guildhall):
                self.states[self.current_player.owner]['captured_states'] += 1
                self.states[tile.owner]['state'].lose_game_state()
                del self.states[tile.owner]
                del self.states_names[self.states_names.index(tile.owner)]
                self.players -= 1

            tile.set_game_unit(unit)
            if tile.owner != self.current_player.owner:
                tile.game_unit.moved = True
            if tile.owner and tile.game_unit.moved:
                if tile.owner in self.states:
                    self.states[tile.owner]['state'].lose_tile(tile)
            self.current_player.new_tile(tile)
            if isinstance(unit, Farm):
                self.current_player.farms += 1
            self.states[self.current_player.owner]['spent_money'] += unit.cost
            tile.color = self.current_player.tiles[0].color
            tile.owner = self.current_player.owner
            if isinstance(unit, Unit):
                self.current_player.earnings -= unit.pay
            self.current_player.money -= unit.cost
            self.count_player_earnings()
            return True

    def move(self, tile_from, tile_to):
        if self.available_move(tile_from) and isinstance(tile_from.game_unit, Unit):
            unit = tile_from.game_unit
            if (tile_to in available_tiles(self.grid, tile_from, unit.power, unit.steps,
                                           tile_from.owner)) and not tile_from.game_unit.moved:
                self.operational_list.append((self.grid.grid.copy(), self.states.copy()))
                try:
                    if tile_to.owner:
                        self.states[tile_to.owner]['state'].lose_tile(tile_to)
                except Exception:
                    pass
                if isinstance(tile_to.game_unit, Guildhall):
                    self.states[self.current_player.owner]['captured_states'] += 1
                    self.states[tile_to.owner]['state'].lose_game_state()
                    del self.states[tile_to.owner]
                    del self.states_names[self.states_names.index(tile_to.owner)]
                    self.players -= 1
                tile_from.game_unit = None
                tile_to.owner = tile_from.owner
                tile_to.color = tile_from.color
                tile_to.set_game_unit(unit)
                tile_to.game_unit.moved = True
                self.states[tile_from.owner]['state'].new_tile(tile_to)
                self.count_player_earnings()
