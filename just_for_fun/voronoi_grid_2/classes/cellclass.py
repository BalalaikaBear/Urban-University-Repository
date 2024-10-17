import math
from typing import Optional
from just_for_fun.voronoi_grid_2.constants.biomes import Biomes

class Cell:
    __slots__ = ['node', 'edges', 'corners', 'state']

    def __init__(self,
                 node: tuple[float, float],
                 edges: Optional[list['Cell']] = None,
                 corners: Optional[list[tuple[float, float]]] = None,
                 state: Biomes = Biomes.NONE) -> None:
        """
        :param node: координата ячейки
        :param edges: соседние ячейки
        :param corners: контур ячейки
        :param state: состояние ячейки
        """
        self.node = node
        self.edges = [] if edges is None else edges
        self.corners = [] if corners is None else corners
        self.state = state

    def add_edges(self, *edges: 'Cell') -> None:
        """Добавляет соседние ячейки в список и сортирует их по часовой стрелке"""
        for edge in edges:
            self.edges.append(edge)
        self.edges = sorted(self.edges, key=lambda point: math.atan2(point.node[1] - self.node[1],
                                                                     point.node[0] - self.node[0]))

    def add_corners(self, *corners: tuple[float, float]) -> None:
        """Добавляет координат края ячейки в список и сортирует их по часовой стрелке"""
        for corner in corners:
            self.corners.append(corner)
        self.corners = sorted(self.corners, key=lambda point: math.atan2(point[1] - self.node[1],
                                                                         point[0] - self.node[0]))

    def set_state(self, state: Biomes) -> None:
        """Задает состояние ячейки"""
        if isinstance(state, Biomes):
            self.state = state
        else:
            raise TypeError(f'object {state} is not Biomes(Flag)')

    def add_state(self, *states: Biomes) -> None:
        """Добавляет состояние ячейки"""
        for state in states:
            if isinstance(state, Biomes):
                self.state = self.state | state
            else:
                raise TypeError(f'object {state} is not Biomes(Flag)')

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.node[0]}, {self.node[1]})'

if __name__ == '__main__':
    print(Biomes.HILL | Biomes.COAST)
    cell = Cell((1, 2), [Cell((1, 1)), Cell((2, 2))], [(1, 0), (-3, -2)], Biomes.HILL)
    cell.add_edges(Cell((0, 3)), Cell((-2, 11)))
    cell.add_corners((4, 2), (-1, 1), (3, 3))
    print(cell.corners)
