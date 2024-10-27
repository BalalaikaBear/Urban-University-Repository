import random, math, numpy
from typing import Self
from enum import IntEnum, auto
from scipy.spatial import Voronoi, Delaunay, voronoi_plot_2d
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise

from just_for_fun.voronoi_grid_2.classes.hexclass import Hex
from just_for_fun.voronoi_grid_2.classes.cells_data import CellsMap
from just_for_fun.voronoi_grid_2.classes.cellclass import Cell
from just_for_fun.voronoi_grid_2.generators.worldgen import WorldGen
from just_for_fun.voronoi_grid_2.constants.biomes import Biomes
import pygame.math

random.seed(1)

sqrt3 = math.sqrt(3)
noise = PerlinNoise(seed=1)

CHUNK_SIZE = 10  # количество ячеек на одной из граней шестиугольника

def random_lerp(pos_a: tuple[float, float],
                pos_b: tuple[float, float],
                t: float) -> tuple[float, float]:
    """Линейная интерполяция между двумя точками со случайным смещением"""
    # координаты точки, после интерполяции
    point: tuple[float, float] = (pygame.math.lerp(pos_a[0], pos_b[0], t),
                                  pygame.math.lerp(pos_a[1], pos_b[1], t))

    # нормаль к линии интерполяции
    vector_norm = pygame.Vector2(pos_b[1] - pos_a[1],
                                 pos_a[0] - pos_b[0]).normalize()

    # исключение определения двух нормалей к линии
    if pos_b[0] >= pos_a[0]:
        vector_norm = -vector_norm

    # смещение точки вдоль нормали
    offset: float = noise.noise(point) * 0.8

    # новая координата точки
    return (point[0] + vector_norm[0]*offset,
            point[1] + vector_norm[1]*offset)

def lerp(pos_a: tuple[float, float],
         pos_b: tuple[float, float],
         t: float) -> tuple[float, float]:
    """Линейная интерполяция между двумя точками"""
    return (pygame.math.lerp(pos_a[0], pos_b[0], t),
            pygame.math.lerp(pos_a[1], pos_b[1], t))

def square_length(a: tuple[float, float], b: tuple[float, float]) -> float:
    return (b[0]-a[0])**2 + (b[1]-a[1])**2

class ChunkState(IntEnum):
    INIT = auto()
    RELAXING = auto()
    GEN_CELLS = auto()
    DONE = auto()

class ChunkGen:
    def __init__(self, coordinate: Hex) -> None:
        # координаты чанка
        self.coordinate = coordinate
        self._x_offset: float = coordinate.q * CHUNK_SIZE*3/2
        self._y_offset: float = coordinate.r * CHUNK_SIZE*sqrt3 + coordinate.q * CHUNK_SIZE*sqrt3/2

        # состояние чанка
        self.state = ChunkState.INIT
        self.relax_iter = 0  # количество проходов расслабляющего алгоритма

        # центры ячеек
        self.points = []  # все точки чанка

        # Voronoi и Delaunay объекты
        self.vor = None

    @property
    def corners(self) -> list[tuple[float, float]]:
        """Возвращает координаты вершин шестиугольника"""
        return self.points[:6]

    @property
    def edge_points(self) -> list[tuple[float, float]]:
        """Возвращает координаты точек на ребрах шестиугольника"""
        return self.points[6:CHUNK_SIZE*6]

    def run(self):
        self.generate_all_points()

    def generate_all_points(self) -> None:
        """
        Генерация сетки в первом приближении

        :return: Грубая диаграмма Вороного
        """
        # изменение состояния чанка
        self.state = ChunkState.RELAXING

        # сброс ячеек
        self.points = []  # [<corners>, <edge_points>, <inside_points>]

        # вершины шестиугольника
        for i in range(6):
            angle_deg = 60 * i
            angle_rad = math.radians(angle_deg)
            coordinate = (self._x_offset + CHUNK_SIZE * math.cos(angle_rad),
                          self._y_offset + CHUNK_SIZE * math.sin(angle_rad))
            self.points.append(coordinate)

        # генерация точек на ребрах шестиугольника
        for i in range(6):
            for step in [x / CHUNK_SIZE for x in range(1, CHUNK_SIZE)]:
                if i == 5:
                    coordinate = random_lerp(self.points[i], self.points[0], step)
                    self.points.append(coordinate)
                else:
                    coordinate = random_lerp(self.points[i], self.points[i + 1], step)
                    self.points.append(coordinate)

        # генерация точек внутри шестиугольника
        while len(self.points) < CHUNK_SIZE**2 * 3 + CHUNK_SIZE*6:
            x = (random.random()-0.5) * CHUNK_SIZE*1.8 + self._x_offset
            y = (random.random()-0.5) * CHUNK_SIZE*1.6 + self._y_offset
            if self._in_bounds(x, y, accuracy=0.9):
                self.points.append((x, y))

        # Voronoi
        self.vor = Voronoi(self.points, incremental=True)

    def relax_points_inside(self) -> None:
        """
        Алгоритм релаксации для диаграммы Вороного

        :return: Новое положение ячеек шестиугольника
        """
        # изменение состояния чанка
        self.state = ChunkState.RELAXING
        self.relax_iter += 1

        # Calculating the area and centroid of a polygon - https://paulbourke.net/geometry/polygonmesh/
        # Lloyd's algorithm - https://en.wikipedia.org/wiki/Lloyd%27s_algorithm
        self.points = self.points[:CHUNK_SIZE*6]  # сброс ячеек
        for segment_index in self.vor.point_region[CHUNK_SIZE*6:]:
            # список с повторяемым первым элементом
            vertice_indexes_in_segment: list = self.vor.regions[segment_index]+self.vor.regions[segment_index][0:1]

            # определение центра образованного полигона
            area, center_x, center_y = 0, 0, 0
            for index, i in enumerate(vertice_indexes_in_segment):
                if index == len(vertice_indexes_in_segment)-1:
                    break
                j = vertice_indexes_in_segment[index+1]
                v0 = self.vor.vertices[i]  # текущая координата из списка
                v1 = self.vor.vertices[j]  # следующая координата из списка
                cross = v0[0]*v1[1] - v1[0]*v0[1]
                area += cross
                center_x += (v0[0]+v1[0])*cross
                center_y += (v0[1]+v1[1])*cross
            area = area/2
            center_x /= 6*area
            center_y /= 6*area

            # защита от покидания ячеек сетки
            if self._in_bounds(center_x, center_y, accuracy=0.95):
                self.points.append((center_x, center_y))

        self.vor = Voronoi(self.points, incremental=True)

    def generate_cells(self, map_data: CellsMap) -> None:
        """Создание ячеек на карте"""
        # изменение состояния чанка
        self.state = ChunkState.GEN_CELLS

        for point_index, point in enumerate(self.vor.points):  # ... in [x, y]
            # положение ячейки (координата центра ячейки)
            cell_node: tuple[float, float] = round(float(point[0]), 5), round(float(point[1]), 5)

            # координаты соседних ячеек
            cell_edges: list[tuple[float, float]] = []
            for ridge_point_index in self.vor.ridge_points:  # ... in [индекс точки, индекс точки]
                if point_index == ridge_point_index[0]:
                    # исключение ячеек, расстояние между которыми больше заданного числа
                    if square_length(point, self.vor.points[ridge_point_index[1]]) < 2:
                        cell_edges.append((round(float(self.vor.points[ridge_point_index[1]][0]), 5),
                                           round(float(self.vor.points[ridge_point_index[1]][1]), 5)))
                if point_index == ridge_point_index[1]:
                    # исключение ячеек, расстояние между которыми больше заданного числа
                    if square_length(point, self.vor.points[ridge_point_index[0]]) < 2:
                        cell_edges.append((round(float(self.vor.points[ridge_point_index[0]][0]), 5),
                                           round(float(self.vor.points[ridge_point_index[0]][1]), 5)))

            # генерация ячейки
            map_data.add(cell_node, cell_edges, WorldGen(1).cell_type(cell_node))

        # удаление vor для освобождения памяти
        del self.vor

    def _in_bounds(self, x: float, y: float, accuracy: float = 1) -> bool:
        """Проверка координат внутри шестиугольника"""
        if ((self._x_offset - x - CHUNK_SIZE*accuracy) * sqrt3 + self._y_offset
                < y < (self._x_offset - x + CHUNK_SIZE*accuracy) * sqrt3 + self._y_offset
                and (x - self._x_offset - CHUNK_SIZE*accuracy) * sqrt3 + self._y_offset
                < y < (x - self._x_offset + CHUNK_SIZE*accuracy) * sqrt3 + self._y_offset
                and -sqrt3*CHUNK_SIZE + self._y_offset < y < sqrt3*CHUNK_SIZE + self._y_offset):
            return True
        else:
            return False

    def __repr__(self):
        return f'ChunkGrid(coordinate={self.coordinate}, state={self.state})'

if __name__ == '__main__':
    chunk = ChunkGen(coordinate=Hex(1, 0))
    chunk.generate_all_points()
    for _ in range(20):
        chunk.relax_points_inside()

    print(chunk.corners)
    print("vor.POINTS:", len(chunk.vor.points), chunk.vor.points)
    print("vor.REGIONS:", len(chunk.vor.regions), chunk.vor.regions)
    fig = voronoi_plot_2d(chunk.vor)
    plt.show()
