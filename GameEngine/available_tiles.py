from GameEngine.HexGrid import HexGrid
from GameEngine.Tile import HexTile
from GameEngine.tile_defense import tile_defense
from GameEngine.GameUnits.Obstacles import Obstacles


def available_tiles(grid: HexGrid, cur_tile: HexTile, power, step: int, owner):
    unchecked = {cur_tile.indexes: step}
    to_check = {}
    checked = {}
    res = []
    while unchecked and step:
        for tile_indexes in unchecked:
            i, j = tile_indexes
            for tile in grid.get_adjacent_tiles(i, j):
                if tile.indexes in checked.keys() and step <= checked[tile.indexes]:
                    continue
                checked[tile.indexes] = step
                if tile_defense(grid, tile.indexes, owner) < power:
                    if owner != tile.owner:
                        res.append(tile)
                    else:
                        if tile.game_unit is None:
                            res.append(tile)
                            to_check[tile.indexes] = step
                        elif isinstance(tile.game_unit, Obstacles):
                            res.append(tile)

        unchecked = to_check
        to_check = {}
        step -= 1

    return res
