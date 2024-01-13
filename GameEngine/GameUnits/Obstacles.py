from GameEngine.GameUnits.GameUnit import GameUnit


class Obstacles(GameUnit):
    def __init__(self, image_path: str, scale: float, power: int = 0):
        super().__init__(image_path, scale)
        self.power = power


class Tree(Obstacles):
    def __init__(self, path='tree32.png', scale=2):
        super().__init__(path, scale, power=0)


class Grave(Obstacles):
    def __init__(self, path='grave32.png', scale=2):
        super().__init__(path, scale, power=0)


class Rock(Obstacles):
    def __init__(self, path='rock32.png', scale=2):
        super().__init__(path, scale, power=2)
