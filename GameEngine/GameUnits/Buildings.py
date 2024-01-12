from GameEngine.GameUnits.GameUnit import GameUnit


class Building(GameUnit):
    def __init__(self, image_path: str, scale: float, power: int = 0, cost: int = 0):
        super().__init__(image_path, scale)
        self.power = power
        self.cost = cost

    def to_string(self):
        return 'Building'


class Farm(Building):
    def __init__(self, scale):
        super().__init__("farm32.png", scale, power=0, cost=12)

    def to_string(self):
        return 'Farm'


class Guildhall(Building):
    def __init__(self, scale):
        super().__init__("guildhall32.png", scale, power=2)

    def to_string(self):
        return 'Guildhall'


class TowerFirst(Building):
    def __init__(self, scale):
        super().__init__("towerfirst32.png", scale, power=2, cost=15)

    def to_string(self):
        return 'TowerFirst'


class TowerSecond(Building):
    def __init__(self, scale):
        super().__init__("towersecond32.png", scale, power=3, cost=35)

    def to_string(self):
        return 'TowerSecond'
