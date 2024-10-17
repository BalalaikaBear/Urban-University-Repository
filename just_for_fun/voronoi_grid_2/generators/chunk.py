import random, math
from typing import Self
from enum import IntEnum, auto
from scipy.spatial import Voronoi, Delaunay, voronoi_plot_2d
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise

from just_for_fun.voronoi_grid_2.classes.hexclass import Hex
import pygame.math

sqrt3 = math.sqrt(3)
noise = PerlinNoise()

CHUNK_SIZE = 12  # количество ячеек на одной из граней шестиугольника

def random_lerp(pos_a: tuple[float, float],
                pos_b: tuple[float, float],
                t: float) -> tuple[float, float]:
    """Линейная интерполяция между двумя точками со случайным смещением"""
    point: tuple[float, float] = (pygame.math.lerp(pos_a[0], pos_b[0], t),
                                  pygame.math.lerp(pos_a[1], pos_b[1], t))
    vector_norm = pygame.Vector2(pos_b[1] - pos_a[1],
                                 pos_a[0] - pos_b[0]).normalize()
    offset: float = noise.noise(point) * 0.2
    return (point[0] + vector_norm[0]*offset,
            point[1] + vector_norm[1]*offset)

def lerp(pos_a: tuple[float, float],
         pos_b: tuple[float, float],
         t: float) -> tuple[float, float]:
    """Линейная интерполяция между двумя точками"""
    return (pygame.math.lerp(pos_a[0], pos_b[0], t),
            pygame.math.lerp(pos_a[1], pos_b[1], t))

class ChunkState(IntEnum):
    INIT = auto()
    RELAXING = auto()
    FREEZE = auto()
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
        self.relax_iter = 0

        # центры ячеек
        self.points = []  # все точки чанка
        self.corners = []  # координаты вершин шестиугольника
        self.edge_points = []  # точки на ребрах шестиугольника

        # Voronoi и Delaunay объекты
        self.vor = None
        self.dl = None

    def run(self):
        self.generate()

    def generate(self) -> None:
        """
        Генерация сетки в первом приближении

        :return: Грубая диаграмма Вороного
        """
        # изменение состояния чанка
        self.state = ChunkState.RELAXING

        # сброс ячеек
        self.points = []
        self.corners = []
        self.edge_points = []

        # вершины шестиугольника
        for i in range(6):
            angle_deg = 60 * i
            angle_rad = math.radians(angle_deg)
            self.corners.append((self._x_offset + CHUNK_SIZE * math.cos(angle_rad),
                                 self._y_offset + CHUNK_SIZE * math.sin(angle_rad)))

        # генерация точек внутри шестиугольника
        while len(self.points) < CHUNK_SIZE**2 * 3:
            x = (random.random()-0.5) * CHUNK_SIZE*1.8 + self._x_offset
            y = (random.random()-0.5) * CHUNK_SIZE*1.6 + self._y_offset
            if (-(x-self._x_offset)*sqrt3 - CHUNK_SIZE*1.6 + self._y_offset < y < -(x-self._x_offset)*sqrt3 + CHUNK_SIZE*1.6 + self._y_offset
                    and (x-self._x_offset)*sqrt3 - CHUNK_SIZE*1.6 + self._y_offset < y < (x-self._x_offset)*sqrt3 + CHUNK_SIZE*1.6 + self._y_offset):
                self.points.append((x, y))

        # генерация точек на ребрах шестиугольника
        for i in range(6):
            for step in [x / CHUNK_SIZE for x in range(CHUNK_SIZE)]:
                if i == 5:
                    self.edge_points.append(lerp(self.corners[i], self.corners[0], step))
                else:
                    self.edge_points.append(lerp(self.corners[i], self.corners[i + 1], step))
        self.points += self.edge_points

        # Voronoi
        self.vor = Voronoi(self.points, incremental=True)

    def update(self) -> None:
        """
        Алгоритм релаксации для диаграммы Вороного

        :return: Новое положение ячеек шестиугольника
        """
        # изменение состояния чанка
        self.state = ChunkState.RELAXING
        self.relax_iter += 1

        # Calculating the area and centroid of a polygon - https://paulbourke.net/geometry/polygonmesh/
        # Lloyd's algorithm - https://en.wikipedia.org/wiki/Lloyd%27s_algorithm
        self.points = []
        for segment in self.vor.regions:
            if segment and not -1 in segment:
                points = [self.vor.vertices[i] for i in segment]
                area = sum((points[i][0] * points[i + 1][1] - points[i + 1][0] * points[i][1]
                            if i != len(segment) - 1
                            else points[i][0] * points[0][1] - points[0][0] * points[i][1]
                            for i in range(len(segment)))) / 2
                center_x = sum(((points[i][0] + points[i + 1][0])
                                * (points[i][0] * points[i + 1][1] - points[i + 1][0] * points[i][1])
                                if i != len(segment) - 1
                                else (points[i][0] + points[0][0])
                                     * (points[i][0] * points[0][1] - points[0][0] * points[i][1])
                                for i in range(len(segment)))) / (6 * area)
                center_y = sum(((points[i][1] + points[i + 1][1])
                                * (points[i][0] * points[i + 1][1] - points[i + 1][0] * points[i][1])
                                if i != len(segment) - 1
                                else (points[i][1] + points[0][1])
                                     * (points[i][0] * points[0][1] - points[0][0] * points[i][1])
                                for i in range(len(segment)))) / (6 * area)
                self.points.append((center_x, center_y))
        self.points += self.edge_points
        self.vor = Voronoi(self.points, incremental=True)

    def freeze(self) -> None:
        # изменение состояния чанка
        self.state = ChunkState.FREEZE
        self.dl = Delaunay(self.points)

    def __repr__(self):
        return f'ChunkGrid(coordinate={self.coordinate}, state={self.state})'

if __name__ == '__main__':
    chunk = ChunkGen(coordinate=Hex(1, 0))
    chunk.generate()

    fig = voronoi_plot_2d(chunk.vor)
    plt.show()
