from GameEngine.GameUnits.GameUnit import GameUnit


class Obstacles(GameUnit):
    def __init__(self, image_path: str, scale: float, power: int = 0):
        super().__init__(image_path, scale)
        self.power = power


class Tree(Obstacles):
    def __init__(self, scale):
        super().__init__('tree.png', scale, power=0)


class Rock(Obstacles):
    def __init__(self, scale):
        super().__init__('rock.png', scale, power=2)