from GameUnit import GameUnit


class Building(GameUnit):
    def __init__(self, image_path: str, scale: float, defense: int = 0):
        super().__init__(image_path, scale)
        self.defense = defense
