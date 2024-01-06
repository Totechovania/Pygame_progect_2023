from GameEngine.GameUnits.GameUnit import GameUnit


class Building(GameUnit):
    def __init__(self, image_path: str, scale: float, power: int = 0, cost: int = 0):
        super().__init__(image_path, scale)
        self.power = power
        self.cost = cost


class Farm(Building):
    def __init__(self, scale):
        super().__init__("farm.png", scale, power=0, cost=12)


class Guildhall(Building):
    def __init__(self, scale):
        super().__init__("guildhall.png", scale, power=2)


class TowerFirst(Building):
    def __init__(self, scale):
        super().__init__("towerfirst.png", scale, power=2, cost=15)


class TowerSecond(Building):
    def __init__(self, scale):
        super().__init__("towersecond.png", scale, power=3, cost=35)
