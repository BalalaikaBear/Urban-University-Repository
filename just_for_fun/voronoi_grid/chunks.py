import random, math

from pygame.math import lerp as py_lerp
from scipy.spatial import Voronoi

sqrt3 = math.sqrt(3)

def lerp(pos_a: tuple[float, float], pos_b: tuple[float, float], t: float) -> tuple[float, float]:
    """Линейная интерполяция между двумя точками в шестиугольной системе координат"""
    return py_lerp(pos_a[0], pos_b[0], t), py_lerp(pos_a[1], pos_b[1], t)

class ChunkGrid:
    CHUNK_SIZE = 20  # количество ячеек на одной из грани шестиугольника

    def __init__(self, coordinate: tuple[int, int]) -> None:
        self.coordinate = coordinate
        self._x_offset: float = coordinate[0] * self.CHUNK_SIZE*3/2
        self._y_offset: float = coordinate[1] * self.CHUNK_SIZE*sqrt3 + coordinate[0] * self.CHUNK_SIZE*sqrt3/2
        self.points = []
        self.corners = []
        self.vor = None

        self.generate()

    def generate(self) -> None:
        """
        Генерация сетки в первом приближении

        :return: Грубая диаграмма Вороного
        """
        # вершины шестиугольника
        for i in range(6):
            angle_deg = 60 * i
            angle_rad = math.radians(angle_deg)
            self.corners.append((self._x_offset + self.CHUNK_SIZE * math.cos(angle_rad),
                                 self._y_offset + self.CHUNK_SIZE * math.sin(angle_rad)))

        # генерация точек внутри шестиугольника
        while len(self.points) < self.CHUNK_SIZE*45:
            x = (random.random()-0.5) * self.CHUNK_SIZE*1.8
            y = (random.random()-0.5) * self.CHUNK_SIZE*1.6
            if (-x*sqrt3 - self.CHUNK_SIZE*1.6 < y < -x*sqrt3 + self.CHUNK_SIZE*1.6
                    and x*sqrt3 - self.CHUNK_SIZE*1.6 < y < x*sqrt3 + self.CHUNK_SIZE*1.6):
                self.points.append((x + self._x_offset, y + self._y_offset))

        # генерация точек на ребрах шестиугольника
        self._edge_points()

        # Voronoi
        self.vor = Voronoi(self.points)

    def _edge_points(self) -> None:
        """
        Интерполирование крайних ячеек шестиугольника

        :return: Добавляет крайние ячейки в общий массив точек
        """
        for i in range(6):
            for step in [x/self.CHUNK_SIZE for x in range(self.CHUNK_SIZE)]:
                if i == 5:
                    self.points.append(lerp(self.corners[i], self.corners[0], step))
                else:
                    self.points.append(lerp(self.corners[i], self.corners[i+1], step))

    def update(self) -> None:
        """
        Алгоритм релаксации для диаграммы Вороного

        :return: Новое положение ячеек шестиугольника
        """
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
        self._edge_points()
        self.vor = Voronoi(self.points)

if __name__ == '__main__':
    chunk = ChunkGrid(coordinate=(1, 0))
