import copy
import math
import numpy
from numpy.linalg import inv


class Orientation:
    """Хранит информацию о матрицах поворота и угле поворота ячеек"""
    def __init__(self, matrix: numpy, angle: int | float, size: int | float) -> None:
        self.matrix = matrix  # матрица поворота
        self.angle = angle  # начальный угол поворота ячеек
        self.size = size  # размер ячеек

    @property
    def reverse(self) -> numpy:
        return inv(self.matrix)


class Layout:
    """Система координат"""
    def __init__(self, start_orientation: Orientation) -> None:
        self.orientation = copy.deepcopy(start_orientation)  # матрица поворота, обратная матрица

        # масштабирование матрицы поворота
        self.orientation.matrix *= start_orientation.size
        self.orientation.matrix[2, 2] = 1

    def translate(self, pos: tuple[int | float]) -> numpy:
        """Переместить систему координат вдоль осей x и y"""
        translate_matrix = numpy.array([[1, 0, pos[0] * CAMERA_SPEED],
                                       [0, 1, pos[1] * CAMERA_SPEED],
                                       [0, 0, 1]])
        self.orientation.matrix = translate_matrix @ self.orientation.matrix

    def rotate(self, angle: int | float) -> numpy:
        """Повернуть систему координат на указанный угол"""
        angle_rad = math.radians(angle) * ROTATION_SPEED
        rotation_matrix = numpy.array([[math.cos(angle_rad), math.sin(angle_rad), 0],
                                      [-math.sin(angle_rad), math.cos(angle_rad), 0],
                                      [0, 0, 1]])
        self.orientation.matrix = rotation_matrix @ self.orientation.matrix
        self.orientation.angle += angle

    def scale(self, scale: int | float) -> numpy:
        """Отмасштабировать систему координат на указанное значение"""
        scaling_matrix = numpy.array([[scale, 0, 0],
                                  [0, scale, 0],
                                  [0, 0, 1]])
        self.orientation.size *= scale
        self.orientation.matrix = scaling_matrix @ self.orientation.matrix

    def set_layout(self, orientation: Orientation) -> None:
        """Задание новой системы координат"""
        self.__init__(orientation)

    def print(self) -> None:
        print(self.orientation.matrix)
