import numpy
from typing import Optional
from mapdata import Map
from celldata import Cell

# Сокращение записи типов объектов
type Hex[q, r] = tuple[float | numpy.ndarray, float | numpy.ndarray]


def square_grid(width: int, height: int, center: Optional[Hex] = None) -> Map:
    """
    Генерация прямоугольной сетки

    :param width: Ширина генерируемой карты
    :param height: Высота генерируемой карты
    :param center: Координата центра генерируемой карты
    :return: Сгенерированная карта
    """
    coordinates: Map = Map()
    grid_height: int = height - 1

    # определение центра сетки
    if center is None:
        center: tuple[int, int] = (width // 2, grid_height // 2)

    # генерация сетки
    offset = 0
    for col in range(width, 0, -1):
        for row in range(int(offset)-1, int(offset) + grid_height):
            hex_pos: Hex = col - center[0] - 1, row - center[1] - 1
            coordinates[hex_pos] = Cell(hex_pos)
        offset += .5

    return coordinates


def hexagonal_grid(radius: int, center: Optional[Hex] = None) -> Map:
    """
    Генерация сетки в форме шестиугольника

    :param radius: Радиус генерируемой карты
    :param center: Координата центра генерируемой карты
    :return: Сгенерированная карта
    """
    coordinates: Map = Map()

    # определение центра сетки
    if center is None:
        center: Hex = (0, 0)

    # генерация сетки
    for q in range(-radius, radius+1):
        for r in range(max(-radius, -q-radius), min(radius, -q+radius)+1):
            hex_pos: Hex = q + center[0], r + center[1]
            coordinates[hex_pos] = Cell(hex_pos)

    return coordinates
