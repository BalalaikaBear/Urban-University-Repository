import random, math
from enum import Enum, auto
from scipy.spatial import Voronoi

from pygame.math import lerp as py_lerp

sqrt3 = math.sqrt(3)

def lerp(pos_a: tuple[float, float], pos_b: tuple[float, float], t: float) -> tuple[float, float]:
    """Линейная интерполяция между двумя точками в шестиугольной системе координат"""
    return py_lerp(pos_a[0], pos_b[0], t), py_lerp(pos_a[1], pos_b[1], t)

class ChunkState(Enum):
    GEN_POINTS = auto()
    RELAXING = auto()
    FREEZE = auto()
    GEN_CELLS = auto()
    DONE = auto()

class ChunkGrid:
    CHUNK_SIZE = 20  # количество ячеек на одной из граней шестиугольника

    def __init__(self, coordinate: tuple[int, int]) -> None:
        # координаты чанка
        self.coordinate = coordinate
        self._x_offset: float = coordinate[0] * self.CHUNK_SIZE*3/2
        self._y_offset: float = coordinate[1] * self.CHUNK_SIZE*sqrt3 + coordinate[0] * self.CHUNK_SIZE*sqrt3/2

        # состояние чанка
        self.state = ChunkState.GEN_POINTS
        self.relax_iter = 0

        # центры ячеек
        self.points = []  # все точки чанка
        self.corners = []  # координаты вершин шестиугольника
        self.edge_points = []  # точки на ребрах шестиугольника

        # Voronoi объект
        self.vor = None

        self.run()

    def run(self):
        self.generate()

    def generate(self) -> None:
        """
        Генерация сетки в первом приближении

        :return: Грубая диаграмма Вороного
        """
        # изменение состояния чанка
        self.state = ChunkState.GEN_POINTS

        # сброс ячеек
        self.points = []
        self.corners = []
        self.edge_points = []

        # вершины шестиугольника
        for i in range(6):
            angle_deg = 60 * i
            angle_rad = math.radians(angle_deg)
            self.corners.append((self.CHUNK_SIZE * math.cos(angle_rad),
                                 self.CHUNK_SIZE * math.sin(angle_rad)))

        # генерация точек внутри шестиугольника
        while len(self.points) < self.CHUNK_SIZE*45:
            x = (random.random()-0.5) * self.CHUNK_SIZE*1.8
            y = (random.random()-0.5) * self.CHUNK_SIZE*1.6
            if (-x*sqrt3 - self.CHUNK_SIZE*1.6 < y < -x*sqrt3 + self.CHUNK_SIZE*1.6
                    and x*sqrt3 - self.CHUNK_SIZE*1.6 < y < x*sqrt3 + self.CHUNK_SIZE*1.6):
                self.points.append((x, y))

        # генерация точек на ребрах шестиугольника
        for i in range(6):
            for step in [x / self.CHUNK_SIZE for x in range(self.CHUNK_SIZE)]:
                if i == 5:
                    self.edge_points.append(lerp(self.corners[i], self.corners[0], step))
                else:
                    self.edge_points.append(lerp(self.corners[i], self.corners[i + 1], step))
        self.points += self.edge_points

        # Voronoi
        self.vor = Voronoi(self.points)

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
                area = sum([points[i][0] * points[i + 1][1] - points[i + 1][0] * points[i][1]
                            if i != len(segment) - 1
                            else points[i][0] * points[0][1] - points[0][0] * points[i][1]
                            for i in range(len(segment))]) / 2
                center_x = sum([(points[i][0] + points[i + 1][0])
                                * (points[i][0] * points[i + 1][1] - points[i + 1][0] * points[i][1])
                                if i != len(segment) - 1
                                else (points[i][0] + points[0][0])
                                     * (points[i][0] * points[0][1] - points[0][0] * points[i][1])
                                for i in range(len(segment))]) / (6 * area)
                center_y = sum([(points[i][1] + points[i + 1][1])
                                * (points[i][0] * points[i + 1][1] - points[i + 1][0] * points[i][1])
                                if i != len(segment) - 1
                                else (points[i][1] + points[0][1])
                                     * (points[i][0] * points[0][1] - points[0][0] * points[i][1])
                                for i in range(len(segment))]) / (6 * area)
                self.points.append((center_x, center_y))
        self.points += self.edge_points
        self.vor = Voronoi(self.points)

    def freeze(self) -> None:
        # изменение состояния чанка
        self.state = ChunkState.FREEZE

        # перемещение локальных координат в абсолютную систему координат
        for i, coordinate in enumerate(self.points):
            self.points[i] = [coordinate[0] + self._x_offset, coordinate[1] + self._y_offset]
        for i, coordinate in enumerate(self.corners):
            self.corners[i] = [coordinate[0] + self._x_offset, coordinate[1] + self._y_offset]
        for i, coordinate in enumerate(self.edge_points):
            self.edge_points[i] = [coordinate[0] + self._x_offset, coordinate[1] + self._y_offset]

        self.vor = Voronoi(self.points)

    def __repr__(self):
        return f'ChunkGrid(coordinate={self.coordinate}, state={self.state})'

if __name__ == '__main__':
    chunk = ChunkGrid(coordinate=(1, 0))
