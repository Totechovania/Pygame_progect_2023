from math import pi, cos, sin


def hexagon_from_center(center_x: float, center_y: float, radius: float) -> list[tuple[int, int]]:
    vertices = []
    start_x = 0
    start_y = radius
    for i in range(6):
        angle = pi / 3 * i
        x = start_x * cos(angle) - start_y * sin(angle)
        y = start_x * sin(angle) + start_y * cos(angle)
        vertices.append((round(x + center_x),
                         round(y + center_y)))
    return vertices


def get_tile_coords(i, j, radius):
    return j * radius * 3 ** 0.5 + i % 2 * radius * 3 ** 0.5 / 2, i * radius * 1.5
