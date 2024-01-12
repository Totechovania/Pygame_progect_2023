import copy

from GameEngine.HexGrid import HexGrid
from GameEngine.Tile import HexTile


def find_separated_groups(grid: HexGrid, tiles: list[HexTile], empty_tiles=False) -> list[list[HexTile]]:
    if not tiles:
        return []
    res = []
    all_unchecked = []
    for tile in tiles:
        all_unchecked.append(tile)

    checked = []
    while all_unchecked:
        group = [all_unchecked[0]]
        cur_unchecked = [all_unchecked[0]]
        all_unchecked.pop(0)
        to_check = []
        while cur_unchecked:
            for tile in cur_unchecked:
                for adjacent_tile in grid.get_adjacent_tiles(tile, empty_tiles):
                    if adjacent_tile in checked:
                        continue
                    checked.append(adjacent_tile)
                    if adjacent_tile in all_unchecked:
                        all_unchecked.remove(adjacent_tile)
                        group.append(adjacent_tile)
                        to_check.append(adjacent_tile)

            cur_unchecked = to_check
            to_check = []
        res.append(group)
    return res
