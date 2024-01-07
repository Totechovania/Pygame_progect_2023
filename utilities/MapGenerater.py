from GameEngine.HexGrid import HexGrid
from GameEngine.Tile import EmptyTile
from GameEngine.GameUnits.Obstacles import Rock, Tree
from GameEngine.GameUnits.Buildings import Guildhall
import shared
from perlin_noise import PerlinNoise
from random import randint, choice
from numpy import floor

from GameEngine.available_tiles import available_tiles


def perlin_noise(size):
    noise = PerlinNoise(octaves=7, seed=randint(10000, 99999))
    amp = 10
    period = 24
    terrain_width = size
    landscale = [[0 for _ in range(terrain_width)] for _ in range(terrain_width)]

    for position in range(terrain_width ** 2):
        x = floor(position / terrain_width)
        z = floor(position % terrain_width)
        y = floor(noise([x / period, z / period]) * amp)
        if int(y) < -2:
            landscale[int(x)][int(z)] = 0
        else:
            landscale[int(x)][int(z)] = 1
    return landscale


def map_generator(scale, enemy):
    names = ['Александр', 'Анна', 'Екатерина', 'Дмитрий', 'Сергей', 'Мария', 'Владимир', 'Ольга', 'Илья', 'Яна',
             'Андрей', 'Павел', 'Елена', 'Роман', 'Елизавета', 'Вячеслав', 'София', 'Антон', 'Виктория', 'Максим',
             'Ксения', 'Артем', 'Юлия', 'Николай', 'Татьяна', 'Денис', 'Кристина', 'Игорь', 'Евгения', 'Кирилл']
    width = randint(10, 20) * scale
    height = randint(10, 20) * scale
    obstacles = randint(5, 10) * scale
    grid = HexGrid.filled(width, height, 40,
                          (20, 20, shared.WIDTH, shared.HEIGHT))
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
        flag = False
        x, y = randint(0, width - 1), randint(0, height - 1)
        if not isinstance(grid[y, x], EmptyTile) and not grid[y, x].game_unit and not grid[y, x].owner:
            owner = enemy
            color = (randint(0, 255), randint(0, 255), randint(0, 255))
            for tile in available_tiles(grid, grid[y, x], 5, 5, owner):
                if tile.owner:
                    flag = True
            if flag:
                continue
            grid[y, x].owner = owner
            grid[y, x].color = color
            grid[y, x].set_game_unit(Guildhall(2))
            enemy -= 1
            tiles = 4
            while tiles != 0:
                for tile in grid.get_adjacent_tiles(y, x):
                    if not isinstance(tile, EmptyTile) and not tile.owner:
                        tile.owner = owner
                        tile.color = color
                        tiles -= 1
                        if tiles == 0:
                            break
                while True:
                    if tiles != 0:
                        try:
                            y1, x1 = choice(list(grid.get_adjacent_tiles(y, x))).indexes
                            if not isinstance(grid[y1, x1], EmptyTile) and grid[y1, x1].owner == owner:
                                x = x1
                                y = y1
                                break
                        except Exception:
                            pass
                    else:
                        break
    return grid
