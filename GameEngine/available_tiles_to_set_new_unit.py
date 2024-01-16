from GameEngine.tile_defense import tile_defense
from GameEngine.GameUnits.Units import *
from GameEngine.GameUnits.Obstacles import Rock


def available_tiles_to_set_new_unit(grid, state_tiles, current_player, unit_to_set):
    res = []
    for i in state_tiles:
        neighbours = grid.get_adjacent_tiles(i)
        for j in neighbours:
            if j.owner != current_player.owner:
                if unit_to_set == Peasant:
                    if tile_defense(grid, j) < 1 and not isinstance(j.game_unit, Rock):
                        res.append(j)
                elif unit_to_set == Spearman:
                    if tile_defense(grid, j) < 2 and not isinstance(j.game_unit, Rock):
                        res.append(j)
                elif unit_to_set == Warrior:
                    if tile_defense(grid, j) < 3:
                        res.append(j)
                elif unit_to_set == Knight:
                    res.append(j)
    for i in state_tiles:
        res.append(i)
    return res
