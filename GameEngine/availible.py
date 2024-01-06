from GameEngine.HexGrid import HexGrid
from GameEngine.Tile import HexTile
from tile_defense import tile_defense
from GameEngine.GameUnits.Trees import Tree


def available_tiles(grid: HexGrid, cur_tile: HexTile, power, step: int, owner, checked: list[HexTile] | None = None):
    if checked is None:
        checked = []
    res = []
    if step == 0:
        return res
    i, j = cur_tile.indexes
    for tile in grid.get_adjacent_tiles(i, j):
        if tile not in checked:
            checked.append(tile)
            if tile_defense(grid, tile.indexes, owner) < power:
                if owner != tile.owner:
                    res.append(tile)
                else:
                    if tile.game_unit is None:
                        res.append(tile)
                        res.extend(available_tiles(grid, tile, power, step - 1, owner, checked))
                    elif isinstance(tile.game_unit, Tree):
                        res.append(tile)

    return res
