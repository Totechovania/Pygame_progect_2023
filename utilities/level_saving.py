import os
import json


def save_level(save_dir, level_name, players, grid_str):
    level_dir = str(os.path.join(save_dir, level_name))
    if not os.path.exists(level_dir):
        os.mkdir(level_dir)
    with open(os.path.join(level_dir, 'players.json'), 'w', encoding='utf-8') as f:
        json.dump(players, f, ensure_ascii=False)
    with open(os.path.join(level_dir, 'grid.txt'), 'w', encoding='utf-8') as f:
        f.write(grid_str)


def load_level(save_dir, level_name):
    level_dir = str(os.path.join(save_dir, level_name))
    with open(os.path.join(level_dir, 'players.json'), encoding='utf-8') as f:
        players = json.load(f)
    with open(os.path.join(level_dir, 'grid.txt'), encoding='utf-8') as f:
        grid_str = f.read()
    return players, grid_str
