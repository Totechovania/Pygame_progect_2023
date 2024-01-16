import os
import json


def save_level(save_dir, level_name, players, grid_str):
    level_dir = str(os.path.join(save_dir, level_name))
    if not os.path.exists(level_dir):
        os.mkdir(level_dir)
    with open(os.path.join(level_dir, 'players.json'), 'w') as f:
        json.dump(players, f)
    with open(os.path.join(level_dir, 'grid.txt'), 'w') as f:
        f.write(grid_str)


def load_level(save_dir, level_name, grid):
    level_dir = str(os.path.join(save_dir, level_name))
    with open(os.path.join(level_dir, 'players.json')) as f:
        players = json.load(f)
    with open(os.path.join(level_dir, 'grid.txt')) as f:
        grid_str = f.read()
    grid.tiles_from_string(grid_str)
    return players, grid
