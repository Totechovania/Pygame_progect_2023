from GameUnit import GameUnit


class Tree(GameUnit):
    def __init__(self, image_path: str, scale: float, power: int = 0):
        super().__init__(image_path, scale)
        self.power = power
        