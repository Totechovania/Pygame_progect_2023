from GameEngine.Tile import HexTile, EmptyTile
from GameEngine.GameUnits.Units import Unit
from GameEngine.GameUnits.Buildings import Building
from GameEngine.GameUnits.Obstacles import Obstacles


def tile_defense(grid, tile: tuple[int, int] | HexTile, owner) -> int:
    if isinstance(tile, HexTile):
        indexes = tile.indexes
    else:
        indexes = tile
    adjacent_tiles = grid.get_adjacent_tiles(indexes)

    def tile_aggressive(tile):
        return ((not isinstance(tile, EmptyTile)) and
                (isinstance(tile.game_unit, Unit) or isinstance(tile.game_unit, Building))
                and owner != tile.owner)

    adjacent_tiles = list(filter(tile_aggressive, adjacent_tiles))
    if isinstance(grid[indexes].game_unit, Obstacles):
        adjacent_tiles.append(grid[indexes])

    return max(map(lambda tile: tile.game_unit.power, adjacent_tiles), default=0)


