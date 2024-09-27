import copy, math, numpy
from numpy.linalg import inv
from settings import Player, Camera, Screen, Settings
from hexmath import *

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
    def __init__(self, start_orientation: Orientation, player: Player) -> None:
        self.player = player  # для конкретного игрока

        self.orientation = copy.deepcopy(start_orientation)  # матрица поворота, обратная матрица

        # масштабирование матрицы поворота
        self.orientation.matrix *= start_orientation.size
        self.orientation.matrix[2, 2] = 1

        self._qvector = None
        self._rvector = None
        self.calculate_vectors()


    def translate(self, pos: tuple[int | float]) -> numpy.ndarray:
        """Переместить систему координат вдоль осей x и y"""
        translate_matrix = numpy.array([[1, 0, pos[0] * self.player.settings.camera.movement],
                                       [0, 1, pos[1] * self.player.settings.camera.movement],
                                       [0, 0, 1]])
        self.orientation.matrix = translate_matrix @ self.orientation.matrix
        self.calculate_vectors()

    def rotate(self, angle: int | float) -> numpy.ndarray:
        """Повернуть систему координат на указанный угол"""
        angle_rad = math.radians(angle) * self.player.settings.camera.rotation
        rotation_matrix = numpy.array([[math.cos(angle_rad), math.sin(angle_rad), 0],
                                      [-math.sin(angle_rad), math.cos(angle_rad), 0],
                                      [0, 0, 1]])
        self.orientation.matrix = rotation_matrix @ self.orientation.matrix
        self.orientation.angle += angle * self.player.settings.camera.rotation
        self.calculate_vectors()

    def scale(self, scale: int | float) -> numpy.ndarray:
        """Отмасштабировать систему координат на указанное значение"""
        scaling_matrix = numpy.array([[scale * self.player.settings.camera.scale, 0, 0],
                                     [0, scale * self.player.settings.camera.scale, 0],
                                     [0, 0, 1]])
        self.orientation.matrix = scaling_matrix @ self.orientation.matrix
        self.orientation.size *= scale * self.player.settings.camera.scale
        self.calculate_vectors()

    def calculate_vectors(self) -> None:
        """Определение векторов (1, 0) и (0, 1) для последующего быстрого вычисления"""
        self._qvector = hex_to_pixel(self, (1, 0), self.player.settings.screen.origin)
        self._rvector = hex_to_pixel(self, (0, 1), self.player.settings.screen.origin)

    def get(self, hex_coord: tuple[int | float]) -> tuple[int | float, int | float]:
        """Возвращает координаты новой системы координат"""
        return (self._qvector[0] * hex_coord[0] + self._rvector[0] * hex_coord[1],
                self._qvector[1] * hex_coord[0] + self._rvector[1] * hex_coord[1])

    def set_layout(self, orientation: Orientation) -> None:
        """Задание новой системы координат"""
        self.__init__(orientation)

    def print(self) -> None:
        print(self.orientation.matrix)
