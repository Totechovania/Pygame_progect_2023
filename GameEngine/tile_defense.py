from Tile import EmptyTile
from GameEngine.GameUnits.Units import Unit
from GameEngine.GameUnits.Buildings import Building


def tile_defense(grid, x, y, owner) -> int:
    adjacent_tiles = grid.get_adjacent_tiles(x, y)

    def tile_aggressive(tile):
        return ((not isinstance(tile, EmptyTile)) and
                (isinstance(tile.game_unit, Unit) or isinstance(tile.game_unit, Building))
                and owner != tile.owner)

    adjacent_tiles = filter(tile_aggressive, adjacent_tiles)

    return max(map(lambda tile: tile.game_unit.power, adjacent_tiles))


