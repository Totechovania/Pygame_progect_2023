from GameEngine.HexGrid import HexGrid
from GameEngine.Tile import HexTile
from GameEngine.tile_defense import tile_defense
from GameEngine.GameUnits.Obstacles import Obstacles
from GameEngine.GameUnits.Units import Unit, Knight
from GameEngine.GameUnits.Buildings import Building


def available_tiles(grid: HexGrid, cur_tile: HexTile or tuple[int, int], power=None, step: int = None, owner=None,
                    unit=None):
    if not isinstance(cur_tile, HexTile):
        cur_tile = grid[cur_tile]
    if power is None:
        if cur_tile.game_unit is not None:
            power = tile_defense(grid, cur_tile)
        else:
            power = 0
    if step is None:
        if cur_tile.game_unit is not None:
            step = cur_tile.game_unit.steps
        else:
            step = 0
    if unit is None:
        unit = cur_tile.game_unit
    if owner is None:
        owner = cur_tile.owner

    unchecked = {cur_tile.indexes: step}
    to_check = {}
    checked = {}
    res = []

    while unchecked and step:
        for tile_indexes in unchecked:
            for tile in grid.get_adjacent_tiles(tile_indexes):
                if tile.indexes in checked.keys() and step <= checked[tile.indexes]:
                    continue
                checked[tile.indexes] = step
                go_further = True
                if owner != tile.owner:
                    go_further = False
                    tile_power = tile_defense(grid, tile)
                else:
                    tile_power = 0
                if isinstance(tile.game_unit, Obstacles):
                    go_further = False
                    tile_power = max(tile_power, tile.game_unit.power)
                if power > tile_power or isinstance(cur_tile.game_unit, Knight):
                    res.append(tile)
                    if go_further:
                        to_check[tile.indexes] = step
        unchecked = to_check
        to_check = {}
        step -= 1

    res = list(filter(
        lambda t: not (t.owner == owner and (isinstance(t.game_unit, Unit) or isinstance(t.game_unit, Building))), res))

    return res
