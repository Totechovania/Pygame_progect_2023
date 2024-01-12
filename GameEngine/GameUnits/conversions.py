from GameEngine.GameUnits.Units import Peasant, Spearman, Warrior, Knight
from GameEngine.GameUnits.Obstacles import Tree, Grave, Rock
from GameEngine.GameUnits.Buildings import Farm, Guildhall, TowerFirst, TowerSecond


UNIT_TO_STRING = {
    Peasant: 'Peasant',
    Spearman: 'Spearman',
    Warrior: 'Warrior',
    Knight: 'Knight',
    Tree: 'Tree',
    Grave: 'Grave',
    Rock: 'Rock',
    Farm: 'Farm',
    Guildhall: 'Guildhall',
    TowerFirst: 'TowerFirst',
    TowerSecond: 'TowerSecond'
}

UNIT_FROM_STRING = dict((v, k) for k, v in UNIT_TO_STRING.items())


def unit_from_string(string: str, scale: float):
    if string == 'None':
        return None
    return UNIT_FROM_STRING[string](scale)


def unit_to_string(unit):
    if unit is None:
        return 'None'
    return UNIT_TO_STRING[unit.__class__]
