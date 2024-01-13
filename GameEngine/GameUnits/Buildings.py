from GameEngine.GameUnits.GameUnit import GameUnit


class Building(GameUnit):
    def __init__(self, image_path: str, scale: float, power: int = 0, cost: int = 0):
        super().__init__(image_path, scale, 4)
        self.power = power
        self.cost = cost


class Farm(Building):
    def __init__(self, path="farm32.png", scale=2):
        super().__init__(path, scale, power=0, cost=12)


class Guildhall(Building):
    def __init__(self, path='guildhall_animation.png', scale=2):
        super().__init__(path, scale, power=2)


class TowerFirst(Building):
    def __init__(self, path="towerfirst32.png", scale=2):
        super().__init__(path, scale, power=2, cost=15)


class TowerSecond(Building):
    def __init__(self, path="towersecond32.png", scale=2):
        super().__init__(path, scale, power=3, cost=35)
