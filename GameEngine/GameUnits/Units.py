from GameEngine.GameUnits.GameUnit import GameUnit


class Unit(GameUnit):
    def __init__(self, image_path: str, scale: float, cost: int, pay: int, power: int = 0, steps: int = 6):
        super().__init__(image_path, scale)
        self.power = power
        self.steps = steps
        self.pay = pay
        self.cost = cost
        self.moved = False


class Peasant(Unit):
    def __init__(self, scale: float):
        super().__init__('peasant32.png', scale, power=1, steps=6, cost=10, pay=1)


class Spearman(Unit):
    def __init__(self, scale: float):
        super().__init__('spearman32.png', scale, power=2, steps=8, cost=15, pay=5)


class Warrior(Unit):
    def __init__(self, scale: float):
        super().__init__('warrior32.png', scale, power=3, steps=10, cost=30, pay=15)


class Knight(Unit):
    def __init__(self, scale: float):
        super().__init__('knight32.png', scale, power=4, steps=6, cost=40, pay=30)