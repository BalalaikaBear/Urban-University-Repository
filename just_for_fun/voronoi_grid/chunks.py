import random, math
from enum import IntEnum, auto
from scipy.spatial import Voronoi
from typing import Optional

from hexclass import Hex
from pygame.math import lerp as py_lerp

sqrt3 = math.sqrt(3)

def lerp(pos_a: tuple[float, float], pos_b: tuple[float, float], t: float) -> tuple[float, float]:
    """Линейная интерполяция между двумя точками"""
    return py_lerp(pos_a[0], pos_b[0], t), py_lerp(pos_a[1], pos_b[1], t)

class ChunkState(IntEnum):
    INIT = auto()
    RELAXING = auto()
    FREEZE = auto()
    GEN_CELLS = auto()
    DONE = auto()

class Chunk:
    CHUNK_SIZE = 12  # количество ячеек на одной из граней шестиугольника

    def __init__(self, coordinate: Hex) -> None:
        # координаты чанка
        self.coordinate = coordinate
        self._x_offset: float = coordinate.q * self.CHUNK_SIZE*3/2
        self._y_offset: float = coordinate.r * self.CHUNK_SIZE*sqrt3 + coordinate.q * self.CHUNK_SIZE*sqrt3/2

        # состояние чанка
        self.state = ChunkState.INIT
        self.relax_iter = 0

        # центры ячеек
        self.points = []  # все точки чанка
        self.corners = []  # координаты вершин шестиугольника
        self.edge_points = []  # точки на ребрах шестиугольника

        # Voronoi объект
        self.vor = None

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
            self.corners.append((self.CHUNK_SIZE * math.cos(angle_rad),
                                 self.CHUNK_SIZE * math.sin(angle_rad)))

        # генерация точек внутри шестиугольника
        while len(self.points) < self.CHUNK_SIZE**2 * 3:
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
        print('Freeze')

    def __repr__(self):
        return f'ChunkGrid(coordinate={self.coordinate}, state={self.state})'


class ChunksData:
    def __init__(self, **kwargs) -> None:
        INIT = True
        RELAXING = True
        FREEZE = True
        GEN_CELLS = True
        DONE = True

        for key, value in kwargs.items():
            if key == 'INIT':
                self.INIT = value
                INIT = False
            if key == 'RELAXING':
                self.RELAXING = value
                RELAXING = False
            if key == 'FREEZE':
                self.FREEZE = value
                FREEZE = False
            if key == 'GEN_CELLS':
                self.GEN_CELLS = value
                GEN_CELLS = False
            if key == 'DONE':
                self.DONE = value
                DONE = False

        if INIT: self.INIT = {}
        if RELAXING: self.RELAXING = {}
        if FREEZE: self.FREEZE = {}
        if GEN_CELLS: self.GEN_CELLS = {}
        if DONE: self.DONE = {}

    @property
    def size(self) -> int:
        """Возвращает количество чанков в объекте"""
        return (len(self.INIT) +
                len(self.RELAXING) +
                len(self.FREEZE) +
                len(self.GEN_CELLS) +
                len(self.DONE))

    def move(self, input: Chunk | Hex, _from: Optional[ChunkState] = None) -> None:
        if isinstance(input, Chunk):
            if _from is None:
                state = input.state
            else:
                state = _from

            if state is ChunkState.INIT:
                print('init     |', self, self.INIT)
                pop = self.INIT.pop(input.coordinate)
                print('init     |', pop)
                self.RELAXING[input.coordinate] = pop
                print('init     |', self, self.RELAXING)
            elif state is ChunkState.RELAXING:
                print('relaxing |', self, self.RELAXING)
                pop = self.RELAXING.pop(input.coordinate)
                print('relaxing |', pop)
                self.FREEZE[input.coordinate] = pop
                print('relaxing |', self, self.FREEZE)
            elif state is ChunkState.FREEZE:
                self.GEN_CELLS[input.coordinate] = self.FREEZE.pop(input.coordinate)
            elif state is ChunkState.GEN_CELLS:
                self.DONE[input.coordinate] = self.GEN_CELLS.pop(input.coordinate)
            else:
                raise ValueError('Cannot move chunk to higher dict')

        elif isinstance(input, Hex):
            if _from is None:
                state = input
            else:
                state = _from

            if state is ChunkState.INIT:
                self.RELAXING[input] = self.INIT.pop(input)
            elif state is ChunkState.RELAXING:
                self.FREEZE[input] = self.RELAXING.pop(input)
            elif state is ChunkState.FREEZE:
                self.GEN_CELLS[input] = self.FREEZE.pop(input)
            elif state is ChunkState.GEN_CELLS:
                self.DONE[input] = self.GEN_CELLS.pop(input)
            else:
                raise ValueError('Cannot move chunk to higher dict')

    def __contains__(self, item):
        if item in self.INIT: return True
        elif item in self.RELAXING: return True
        elif item in self.FREEZE: return True
        elif item in self.GEN_CELLS: return True
        elif item in self.DONE: return True
        else: return False

    def __str__(self) -> str:
        return (
            f'ChunkData(SIZE={self.size}, [' +
            f'INIT: {len(self.INIT)}, ' +
            f'RELAXING: {len(self.RELAXING)}, ' +
            f'FREEZE: {len(self.FREEZE)}, ' +
            f'GEN_CELLS: {len(self.GEN_CELLS)}, ' +
            f'DONE: {len(self.DONE)}])'
        )

if __name__ == '__main__':
    chunk_data = ChunksData(INIT={Hex(0, 0): Chunk(Hex(0, 0))})
    print(chunk_data.INIT, chunk_data.RELAXING)
    print(chunk_data)
    #chunk = Chunk(coordinate=Hex(1, 0))
