import math, numpy
from typing import Optional
from just_for_fun.voronoi_grid_2.constants.biomes import Biomes

class Cell:
    __slots__ = ['node', 'edges', 'corners', 'states']

    def __init__(self,
                 node: tuple[float, float],
                 edges: list['Cell'] = None,
                 corners: list[tuple[float, float]] = None,
                 state: set[Biomes] = None) -> None:
        """
        :param node: координата ячейки
        :param edges: соседние ячейки
        :param corners: контур ячейки
        :param state: состояние ячейки
        """
        self.node = node
        self.edges = [] if edges is None else edges
        self.corners = [] if corners is None else corners
        self.states = set() if state is None else state

    def add_edges(self, *edges: 'Cell') -> None:
        """Добавляет соседние ячейки в список и сортирует их по часовой стрелке"""
        for edge in edges:
            if edge not in self.edges:
                self.edges.append(edge)
        #self.edges = sorted(self.edges, key=lambda point: math.atan2(point.node[1] - self.node[1],
        #                                                             point.node[0] - self.node[0]))

    def add_corners(self, *corners: tuple[float, float]) -> None:
        """Добавляет координат края ячейки в список и сортирует их по часовой стрелке"""
        for corner in corners:
            if corner not in self.corners:
                self.corners.append(corner)
        self.corners = sorted(self.corners, key=lambda point: math.atan2(point[1] - self.node[1],
                                                                         point[0] - self.node[0]))

    def set_state(self, *states: Biomes) -> None:
        """Задает состояние ячейки"""
        self.states = set(states)

    def add_state(self, *states: Biomes) -> None:
        """Добавляет состояние ячейки"""
        for state in states:
            if isinstance(state, Biomes):
                self.states.add(state)
            else:
                raise TypeError(f'object {state} is not Biomes(Enum)')

    def remove_state(self, *states: Biomes) -> None:
        """Удаляет указанное состояние ячейки"""
        for state in states:
            if isinstance(state, Biomes):
                if state in self.states:
                    self.states.remove(state)
            else:
                raise TypeError(f'object {state} is not Biomes(Enum)')

    def __hash__(self) -> int:
        return hash(self.node)

    def __eq__(self, other) -> bool:
        return (isinstance(other, Cell)
                and self.node == other.node and self.edges == other.edges
                and self.corners == other.corners and self.states == other.states)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.node[0]}, {self.node[1]})'

if __name__ == '__main__':
    cell = Cell((1, 2), [Cell((1, 1)), Cell((2, 2))], [(1, 0), (-3, -2)], {Biomes.HILL})
    cell.add_edges(Cell((0, 3)), Cell((-2, 11)))
    cell.add_corners((4, 2), (-1, 1), (3, 3))
    cell.add_state(Biomes.MOUNTAIN, Biomes.ROAD)
    cell.remove_state(Biomes.OCEAN)
    print(cell.states)
    print(cell.corners)
