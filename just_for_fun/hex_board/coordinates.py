import copy, math, numpy
from numbers import Real  # real numbers as a type
from numpy.linalg import inv
from settings import *

# Сокращение записи типов объектов
type Hex[q, r] = tuple[Real, Real]
type Point[x, y] = tuple[Real, Real]

# Константы
sqrt3: float = math.sqrt(3)

# Кортеж из положений соседних ячеек по часовой стрелке
HEX_DIRECTIONS: tuple = ((1, 0), (1, -1), (0, -1),
                         (-1, 0), (-1, 1), (0, 1))


class Orientation:
    """Хранит информацию о матрицах поворота и угле поворота ячеек"""
    def __init__(self, matrix: numpy.ndarray, angle: int | float = 0, size: int | float = 10) -> None:
        self.matrix = matrix  # матрица поворота
        self.angle = angle  # начальный угол поворота ячеек
        self.size = size  # размер ячеек

    @property
    def reverse(self) -> numpy.ndarray:
        """
        Возвращает обратную матрицу поворота
        """
        return inv(self.matrix)


class Layout:
    """Система координат для конкретного игрока"""
    def __init__(self, start_orientation: Orientation, settings: Settings) -> None:
        self.settings = settings  # для конкретного игрока

        self.orientation = copy.deepcopy(start_orientation)  # матрица поворота, обратная матрица

        # масштабирование матрицы поворота
        self.orientation.matrix *= start_orientation.size
        self.orientation.matrix[2, 2] = 1

        self._qvector = None
        self._rvector = None
        self.calculate_vectors()

    def translate(self, pos: Point) -> None:
        """Переместить систему координат вдоль осей x и y"""
        translate_matrix = numpy.array([[1, 0, pos[0] * self.settings.camera.movement],
                                       [0, 1, pos[1] * self.settings.camera.movement],
                                       [0, 0, 1]])
        self.orientation.matrix = translate_matrix @ self.orientation.matrix
        self.calculate_vectors()

    def rotate(self, angle: int | float) -> None:
        """Повернуть систему координат на указанный угол"""
        angle_rad = math.radians(angle) * self.settings.camera.rotation
        rotation_matrix = numpy.array([[math.cos(angle_rad), math.sin(angle_rad), 0],
                                      [-math.sin(angle_rad), math.cos(angle_rad), 0],
                                      [0, 0, 1]])
        self.orientation.matrix = rotation_matrix @ self.orientation.matrix
        self.orientation.angle += angle * self.settings.camera.rotation
        self.calculate_vectors()

    def scale(self, scale: int | float) -> None:
        """Отмасштабировать систему координат на указанное значение"""
        scaling_matrix = numpy.array([[scale * self.settings.camera.scale, 0, 0],
                                     [0, scale * self.settings.camera.scale, 0],
                                     [0, 0, 1]])
        self.orientation.matrix = scaling_matrix @ self.orientation.matrix
        self.orientation.size *= scale * self.settings.camera.scale
        self.calculate_vectors()

    def calculate_vectors(self) -> None:
        """Определение векторов (1, 0) и (0, 1) для последующего быстрого вычисления"""
        self._qvector = hex_to_pixel(self, (1, 0), self.settings.screen.origin)
        self._rvector = hex_to_pixel(self, (0, 1), self.settings.screen.origin)

    def get_pos(self, hex_coord: Hex) -> Point:
        """Возвращает координаты точки в новой системе координат"""
        return (self._qvector[0] * hex_coord[0] + self._rvector[0] * hex_coord[1],
                self._qvector[1] * hex_coord[0] + self._rvector[1] * hex_coord[1])

    def set_layout(self, orientation: Orientation) -> None:
        """Задание новой системы координат"""
        self.__init__(orientation, self.settings)

    def print(self) -> None:
        print(self.orientation.matrix)


# --------------
# Hexagonal math
def hex_add(hex_a: Hex, hex_b: Hex) -> Hex:
    """Сложение координат ячеек"""
    return hex_a[0] + hex_b[0], hex_a[1] + hex_b[1]

def hex_sub(hex_a: Hex, hex_b: Hex) -> Hex:
    """Вычитание координат ячеек"""
    return hex_a[0] - hex_b[0], hex_a[1] - hex_b[1]

def hex_multi(hex_a: Hex, hex_b: Hex) -> Hex:
    """Умножение координат ячеек"""
    return hex_a[0] * hex_b[0], hex_a[1] * hex_b[1]

def hex_length(hexagon: Hex) -> int:
    """Расстояние до ячейки"""
    return int((abs(hexagon[0]) + abs(hexagon[1])) / 2)

def hex_distance(hex_a: Hex, hex_b: Hex) -> int:
    """Расстояние между двумя ячейками"""
    return hex_length(hex_sub(hex_a, hex_b))

def hex_direction(direction: int) -> Hex:
    """Возвращает ячейку в зависимости от введенного направления"""
    return HEX_DIRECTIONS[direction]

def hex_neighbor(hexagon: Hex, direction: int, *, distance: int = 1) -> Hex | tuple[Hex]:
    """Возвращает следующую ячейку по направлению"""
    if distance == 1:
        return hex_add(hexagon, hex_direction(direction))
    else:
        for _ in range(distance):
            hexagon = hex_add(hexagon, hex_direction(direction))
        return hexagon

def hex_round(hexagon: Hex) -> Hex:
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

def lerp(a: Real, b: Real, t: float) -> float:
    """Линейная интерполяция между двумя точками"""
    return a + (b - a) * t

def hex_lerp(hex_a: Hex, hex_b: Hex, t: float) -> Hex:
    """Линейная интерполяция между двумя точками в шестиугольной системе координат"""
    return lerp(hex_a[0], hex_b[0], t), lerp(hex_a[1], hex_b[1], t)

def hex_linedraw(hex_a: Hex, hex_b: Hex) -> list[tuple]:
    """Выводит список из положений ячеек, расположенных между двумя точками"""
    # добавление значение epsilon для смещения крайней точки
    hex_a_nudge: Hex = hex_a[0] + 1e-06, hex_a[1] + 1e-06
    hex_b_nudge: Hex = hex_b[0] + 1e-06, hex_b[1] + 1e-06
    results = []
    step: float = 1 / max(1, length := hex_distance(hex_a, hex_b))
    for i in range(0, length, step):
        results.append(hex_round(hex_lerp(hex_a_nudge, hex_b_nudge, i)))
    return results

# Преобразования систем координат
def hex_to_pixel(layout: Layout, hexagon: Hex, origin: tuple[int, int]) -> Point:
    """Переводит из шестиугольной (Hexagonal) системы координат в экранную (2D) систему координат """
    # [x, y, 1] = Matrix @ [q, r, 1]
    pixel = layout.orientation.matrix @ numpy.array([hexagon[0], hexagon[1], 1])

    return pixel[0] + origin[0], pixel[1] + origin[1]

def pixel_to_hex(layout, p: Hex, origin: Point) -> Hex:
    """Переводит из экранной (2D) системы координат в шестиугольную (Hexagonal) систему координат"""
    # [q, r, 1] = Reversed Matrix @ [x, y, 1]
    hex_pos = layout.orientation.reverse @ numpy.array([[p[0] - origin[0]],
                                                        [p[1] - origin[1]],
                                                        [1]])
    return hex_pos[0, 0], hex_pos[1, 0]

# стартовая ориентация ячеек
layout_flat = Orientation(numpy.array([[3/2, 0, 0],
                                      [sqrt3/2, sqrt3, 0],
                                      [0, 0, 1]]),
                          angle=0,
                          size=30)

# применяемая система координат (перемещение, масштабирование, начальное положение)
LAYOUT = Layout(layout_flat, settings=settings)
