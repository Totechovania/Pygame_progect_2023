from GameEngine.GameUnits.GameUnit import GameUnit


class Unit(GameUnit):
    def __init__(self, image_path: str, scale: float, power: int = 0, steps: int = 6):
        super().__init__(image_path, scale)
        self.power = power
        self.steps = steps
