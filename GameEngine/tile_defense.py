from GameEngine.Tile import EmptyTile
from GameEngine.GameUnits.Units import Unit
from GameEngine.GameUnits.Buildings import Building
from GameEngine.GameUnits.Trees import Tree


def tile_defense(grid, indexes, owner) -> int:
    i, j = indexes
    adjacent_tiles = grid.get_adjacent_tiles(i, j)

    def tile_aggressive(tile):
        return ((not isinstance(tile, EmptyTile)) and
                (isinstance(tile.game_unit, Unit) or isinstance(tile.game_unit, Building))
                and owner != tile.owner)

    adjacent_tiles = list(filter(tile_aggressive, adjacent_tiles))
    if isinstance(grid[i, j].game_unit, Tree):
        adjacent_tiles.append(grid[i, j])

    return max(map(lambda tile: tile.game_unit.power, adjacent_tiles), default=0)


