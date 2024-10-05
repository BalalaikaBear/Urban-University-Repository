import math
import numpy
from numpy.linalg import inv as numpy_inv
import copy
import hexmath
from settings import Settings

# Сокращение записи типов объектов
type Hex[q, r] = tuple[float | numpy.ndarray, float | numpy.ndarray]
type Point[x, y] = tuple[float | numpy.ndarray, float | numpy.ndarray]

class Orientation:
    """Хранит информацию о матрицах поворота и угле поворота ячеек"""
    def __init__(self, matrix: numpy.ndarray, angle: float = 0, size: float = 10) -> None:
        self.matrix = matrix  # матрица поворота
        self.angle = angle  # начальный угол поворота ячеек
        self.size = size  # размер ячеек

    @property
    def reverse(self) -> numpy.ndarray:
        """
        Возвращает обратную матрицу поворота
        """
        return numpy_inv(self.matrix)


class Layout:
    """Система координат для конкретного игрока"""
    def __init__(self, start_orientation: Orientation, *, settings: Settings) -> None:
        self.settings = settings  # для конкретного игрока

        self.orientation = copy.deepcopy(start_orientation)  # матрица поворота, обратная матрица

        # масштабирование матрицы поворота
        self.orientation.matrix *= self.orientation.size
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

    def rotate(self, angle: float) -> None:
        """Повернуть систему координат на указанный угол"""
        angle_rad = math.radians(angle) * self.settings.camera.rotation
        rotation_matrix = numpy.array([[math.cos(angle_rad), math.sin(angle_rad), 0],
                                      [-math.sin(angle_rad), math.cos(angle_rad), 0],
                                      [0, 0, 1]])
        self.orientation.matrix = rotation_matrix @ self.orientation.matrix
        self.orientation.angle += angle * self.settings.camera.rotation
        self.calculate_vectors()

    def scale(self, scale: float) -> None:
        """Отмасштабировать систему координат на указанное значение"""
        scaling_matrix = numpy.array([[scale, 0, 0],
                                     [0, scale, 0],
                                     [0, 0, 1]])
        self.orientation.matrix = scaling_matrix @ self.orientation.matrix
        self.orientation.size *= scale
        self.calculate_vectors()

    def calculate_vectors(self) -> None:
        """Определение векторов (1, 0) и (0, 1) для последующего быстрого вычисления"""
        self._qvector = hexmath.sub(hexmath.hex_to_pixel(self, (1, 0), settings=self.settings),
                                    hexmath.hex_to_pixel(self, (0, 0), settings=self.settings))
        self._rvector = hexmath.sub(hexmath.hex_to_pixel(self, (0, 1), settings=self.settings),
                                    hexmath.hex_to_pixel(self, (0, 0), settings=self.settings))

    def get_pos(self, hex_coord: Hex) -> Point:
        """Возвращает координаты точки в новой системе координат"""
        return (self.orientation.matrix[0][2] + self.settings.screen.origin[0]
                + self._qvector[0] * hex_coord[0] + self._rvector[0] * hex_coord[1],
                self.orientation.matrix[1][2] + self.settings.screen.origin[1]
                + self._qvector[1] * hex_coord[0] + self._rvector[1] * hex_coord[1])

    def set_layout(self, orientation: Orientation) -> None:
        """Задание новой системы координат"""
        self.__init__(orientation, settings=self.settings)

    def print(self) -> None:
        print(self.orientation.matrix)
