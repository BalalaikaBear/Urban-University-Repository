import numpy

HEX_DIRECTIONS: tuple = ((1, 0), (1, -1), (0, -1),
                         (-1, 0), (-1, 1), (0, 1))  # соседние ячейки по часовой стрелке


# Hexagonal math
def hex_add(hex_a: tuple[int | float], hex_b: tuple[int | float]) -> tuple[int | float]:
    """Сложение координат ячеек"""
    return hex_a[0] + hex_b[0], hex_a[1] + hex_b[1]

def hex_sub(hex_a: tuple[int | float], hex_b: tuple[int | float]) -> tuple[int | float]:
    """Вычитание координат ячеек"""
    return hex_a[0] - hex_b[0], hex_a[1] - hex_b[1]

def hex_multi(hex_a: tuple[int | float], hex_b: tuple[int | float]) -> tuple[int | float]:
    """Умножение координат ячеек"""
    return hex_a[0] * hex_b[0], hex_a[1] * hex_b[1]

def hex_length(hexagon: tuple[int | float]) -> int:
    """Расстояние до ячейки"""
    return int((abs(hexagon[0]) + abs(hexagon[1])) / 2)

def hex_distance(hex_a: tuple[int | float], hex_b: tuple[int | float]) -> int:
    """Расстояние между двумя ячейками"""
    return hex_length(hex_sub(hex_a, hex_b))

def hex_direction(direction: int) -> tuple[int]:
    """Возвращает ячейку в зависимости от введенного направления"""
    return HEX_DIRECTIONS[direction]

def hex_neighbor(hexagon: tuple[int], direction: int, *, length: int = 1) -> tuple[int]:
    """Возвращает следующую ячейку по направлению"""
    if length == 1:
        return hex_add(hexagon, hex_direction(direction))
    else:
        for _ in range(length):
            hexagon = hex_add(hexagon, hex_direction(direction))
        return hexagon

def hex_round(hexagon: tuple[int | float]) -> tuple[int | float]:
    """Возвращает ближайшую ячейку к точке"""
    q = int(round(hexagon[0]))
    r = int(round(hexagon[1]))
    s = int(round(-hexagon[0] - hexagon[1]))
    q_diff = abs(q - hexagon[0])
    r_diff = abs(r - hexagon[1])
    s_diff = abs(s + hexagon[0] + hexagon[1])
    if q_diff > r_diff and q_diff > s_diff:
        q = -r - s
    elif r_diff > s_diff:
        r = -q - s
    else:
        s = -q - r
    return q, r

def lerp(a: int | float, b: int | float, t: float) -> float:
    """Линейная интерполяция между двумя точками"""
    return a + (b - a) * t

def hex_lerp(hex_a: tuple[int | float], hex_b: tuple[int | float], t: float) -> tuple[int | float]:
    """Линейная интерполяция между двумя точками в шестиугольной системе координат"""
    return lerp(hex_a[0], hex_b[0], t), lerp(hex_a[1], hex_b[1], t)

def hex_linedraw(hex_a: tuple[int | float], hex_b: tuple[int | float]) -> list[tuple]:
    """Выводит список из положений ячеек, расположенных между двумя точками"""
    # добавление значение epsilon для смещения крайней точки
    hex_a_nudge: tuple = hex_a[0] + 1e-06, hex_a[1] + 1e-06
    hex_b_nudge: tuple = hex_b[0] + 1e-06, hex_b[1] + 1e-06
    results = []
    step = 1 / max(length := hex_distance(hex_a, hex_b), 1)
    for i in range(0, length, step):
        results.append(hex_round(hex_lerp(hex_a_nudge, hex_b_nudge, i)))
    return results


# Преобразования систем координат
def hex_to_pixel(layout, hexagon: tuple[int | float], origin: tuple[int, int]) -> tuple[float]:
    """Переводит из шестиугольной (Hexagonal) системы координат в экранную (2D) систему координат """
    # [x, y, 1] = Matrix @ [q, r, 1]
    pixel = layout.orientation.matrix @ numpy.array([hexagon[0], hexagon[1], 1])

    return pixel[0] + origin[0], pixel[1] + origin[1]

def pixel_to_hex(layout, p: tuple[int | float], origin: tuple[int, int]):
    """Переводит из экранной (2D) системы координат в шестиугольную (Hexagonal) систему координат"""
    # [q, r, 1] = Reversed Matrix @ [x, y, 1]
    hex_pos = layout.orientation.reverse @ numpy.array([[p[0] - origin[0]],
                                                        [p[1] - origin[1]],
                                                        [1]])

    return hex_pos[0, 0], hex_pos[1, 0]