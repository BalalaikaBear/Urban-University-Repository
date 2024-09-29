import math, numpy
from typing import Callable
from pygame.math import lerp as py_lerp
from settings import Settings

# Сокращение записи типов объектов
type Hex[q, r] = tuple[int | float | numpy.ndarray, int | float | numpy.ndarray]
type Point[x, y] = tuple[int | float | numpy.ndarray, int | float | numpy.ndarray]

_round: Callable = round

# Константы
sqrt3: float = math.sqrt(3)

# Кортеж из положений соседних ячеек по часовой стрелке
HEX_DIRECTIONS: tuple = ((1, 0), (1, -1), (0, -1),
                         (-1, 0), (-1, 1), (0, 1))


# Hexagonal math
def add(hex_a: Hex, hex_b: Hex) -> Hex:
    """Сложение координат ячеек"""
    return hex_a[0] + hex_b[0], hex_a[1] + hex_b[1]


def sub(hex_a: Hex, hex_b: Hex) -> Hex:
    """Вычитание координат ячеек"""
    return hex_a[0] - hex_b[0], hex_a[1] - hex_b[1]


def multi(hex_a: Hex, hex_b: Hex) -> Hex:
    """Умножение координат ячеек"""
    return hex_a[0] * hex_b[0], hex_a[1] * hex_b[1]


def length(hexagon: Hex) -> int:
    """Расстояние до ячейки"""
    return int((abs(hexagon[0]) + abs(hexagon[1])) / 2)


def distance(hex_a: Hex, hex_b: Hex) -> int:
    """Расстояние между двумя ячейками"""
    return length(sub(hex_a, hex_b))


def direction(direct: int) -> Hex:
    """Возвращает ячейку в зависимости от введенного направления"""
    return HEX_DIRECTIONS[direct]


def neighbor(hexagon: Hex, direct: int, *, dist: int = 1) -> Hex | tuple[Hex]:
    """Возвращает следующую ячейку по направлению"""
    if dist == 1:
        return add(hexagon, direction(direct))
    else:
        for _ in range(dist):
            hexagon = add(hexagon, direction(direct))
        return hexagon


def round(hexagon: Hex) -> Hex:
    """Возвращает ближайшую ячейку к точке"""
    q = int(_round(hexagon[0]))
    r = int(_round(hexagon[1]))
    s = int(_round(-hexagon[0] - hexagon[1]))
    q_diff = abs(q - hexagon[0])
    r_diff = abs(r - hexagon[1])
    s_diff = abs(s + hexagon[0] + hexagon[1])
    if q_diff > r_diff and q_diff > s_diff:
        q = -r - s
    elif r_diff > s_diff:
        r = -q - s
    #else:
    #    s = -q - r
    return q, r


def lerp(hex_a: Hex, hex_b: Hex, t: float) -> Hex:
    """Линейная интерполяция между двумя точками в шестиугольной системе координат"""
    return py_lerp(hex_a[0], hex_b[0], t), py_lerp(hex_a[1], hex_b[1], t)


def hex_linedraw(hex_a: Hex, hex_b: Hex) -> list[tuple]:
    """Выводит список из положений ячеек, расположенных между двумя точками"""
    # добавление значение epsilon для смещения крайней точки
    hex_a_nudge: Hex = hex_a[0] + 1e-06, hex_a[1] + 1e-06
    hex_b_nudge: Hex = hex_b[0] + 1e-06, hex_b[1] + 1e-06
    results = []
    _step: float = 1 / max(1, _length := distance(hex_a, hex_b))
    for i in range(0, _length, _step):
        results.append(round(lerp(hex_a_nudge, hex_b_nudge, i)))
    return results


# Преобразования систем координат
def hex_to_pixel(layout, hexagon: Hex, settings: Settings) -> Point:
    """
    Переводит из шестиугольной (Hexagonal) системы координат в экранную (2D) систему координат

    :param layout: Система координат
    :param hexagon: Координаты ячейки [q, r]
    :param settings: Центр экрана
    :return:
    """
    # [x, y, 1] = Matrix @ [q, r, 1]
    pixel = layout.orientation.matrix @ numpy.array([hexagon[0], hexagon[1], 1])
    return pixel[0] + settings.screen.origin[0], pixel[1] + settings.screen.origin[1]


def pixel_to_hex(layout, p: Hex, settings: Settings) -> Hex:
    """
    Переводит из экранной (2D) системы координат в шестиугольную (Hexagonal) систему координат

    :param layout: Система координат
    :param p: Координаты пикселя [x, y]
    :param settings: Центр экрана
    :return:
    """
    # [q, r, 1] = Reversed Matrix @ [x, y, 1]
    hex_pos = layout.orientation.reverse @ numpy.array([[p[0] - settings.screen.origin[0]],
                                                        [p[1] - settings.screen.origin[1]],
                                                        [1]])
    return hex_pos[0, 0], hex_pos[1, 0]
