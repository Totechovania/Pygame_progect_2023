from random import randint
from GameEngine.HexGrid import HexGrid
from GameEngine.Tile import EmptyTile
from GameEngine.GameUnits.Obstacles import Rock, Tree
import shared
from perlin_noise import PerlinNoise
from random import randint, choice, shuffle
from numpy import floor


# from GameEngine.avalible import


def perlin_noise(size):
    noise = PerlinNoise(octaves=7, seed=randint(10000, 99999))
    amp = 10
    period = 24
    terrain_width = size
    landscale = [[0 for i in range(terrain_width)] for i in range(terrain_width)]

    for position in range(terrain_width ** 2):
        x = floor(position / terrain_width)
        z = floor(position % terrain_width)
        y = floor(noise([x / period, z / period]) * amp)
        if int(y) < -2:
            landscale[int(x)][int(z)] = 0
        else:
            landscale[int(x)][int(z)] = 1
    return landscale


def map_generator(scale):
    width = randint(10, 20) * scale
    height = randint(10, 20) * scale
    obstacles = randint(5, 10) * scale
    enemy = randint(2, 5) * scale
    enemy_list = [['yellow', (255, 190, 11)], ['pink', (255, 0, 110)], ['orange', (251, 86, 7)],
                  ['violet', (131, 56, 236)], ['blue', (58, 134, 255)]]
    shuffle(enemy_list)
    grid = HexGrid.filled(width, height, 40,
                          (20, 20, round(shared.WIDTH * 0.8), round(shared.HEIGHT * 0.8)))
    noise = perlin_noise(max(width, height))
    for i in range(width):
        for j in range(height):
            if not noise[i][j]:
                grid.set_empty(j, i)
    while obstacles != 0:
        x, y = randint(0, width - 1), randint(0, height - 1)
        if not isinstance(grid[y, x], EmptyTile) and not grid[y, x].game_unit:
            grid[y, x].set_game_unit(choice([Tree(2), Tree(2), Tree(2), Rock(2)]))
            obstacles -= 1
    while enemy != 0:
        x, y = randint(0, width - 1), randint(0, height - 1)
        if not isinstance(grid[y, x], EmptyTile) and not grid[y, x].game_unit and not grid[y, x].owner:
            owner = enemy_list[0][0]
            color = enemy_list[0][1]
            grid[y, x].owner = owner
            grid[y, x].color = color
            del enemy_list[0]
            enemy -= 1
            tiles = 4
            print(grid[y, x].owner, grid[y, x].indexes)
            while tiles != 0:
                for tile in grid.get_adjacent_tiles(y, x):
                    if not isinstance(tile, EmptyTile) and not tile.owner:
                        tile.owner = owner
                        tile.color = color
                        print(tile.owner, tile.indexes)
                        tiles -= 1
                        if tiles == 0:
                            break
                while True:
                    if tiles != 0:
                        try:
                            x, y = choice(list(grid.get_adjacent_tiles(y, x))).indexes
                            break
                        except Exception:
                            pass
                    else:
                        break


    return grid
