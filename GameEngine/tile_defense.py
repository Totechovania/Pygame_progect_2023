from GameEngine.Tile import HexTile, EmptyTile
from GameEngine.GameUnits.Units import Unit
from GameEngine.GameUnits.Buildings import Building
from GameEngine.GameUnits.Obstacles import Obstacles


def tile_defense(grid, cur_tile: tuple[int, int] or HexTile) -> int:
    if isinstance(cur_tile, HexTile):
        indexes = cur_tile.indexes
    else:
        indexes = cur_tile
        cur_tile = grid[indexes]
    adjacent_tiles = grid.get_adjacent_tiles(indexes)
    owner = cur_tile.owner

    def tile_defends(tile):
        return ((not isinstance(tile, EmptyTile)) and
                (isinstance(tile.game_unit, Unit) or isinstance(tile.game_unit, Building))
                and owner == tile.owner)

    adjacent_tiles = list(filter(tile_defends, adjacent_tiles))

    return max(map(lambda tile: tile.game_unit.power, adjacent_tiles), default=0)


