from mapdata import *
from celldata import *


def generate_square_grid(width: int, height: int, center: Hex = None) -> dict[Hex, Cell]:
    """Генерация прямоугольной сетки"""
    coordinates = {}
    grid_height: int = height - 1

    # определение центра сетки
    if center is None:
        center: Hex = width // 2, grid_height // 2

    # генерация сетки
    offset = 0
    for col in range(width, 0, -1):
        for row in range(int(offset) - 1, int(offset) + grid_height):
            hex_pos: Hex = col - center[0] - 1, row - center[1] - 1
            coordinates[hex_pos] = Cell(hex_pos)
        offset += .5

    return coordinates
