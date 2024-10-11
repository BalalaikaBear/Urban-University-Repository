from collections import namedtuple
from collections.abc import Iterable
from enum import Flag, auto
from typing import Callable, Optional

class Biomes(Flag):
    NONE = auto()

    # roads
    ROAD = auto()
    RAILROAD = auto()

    # land
    GRASSLAND = auto()
    DESERT = auto()
    SAVANNA = auto()
    HILL = auto()

    # forests
    FOREST = auto()
    TUNDRA = auto()
    TAIGA = auto()

    # mountains
    MOUNTAIN = auto()
    VULCANO = auto()

    # water
    RIVER = auto()
    LAKE = auto()
    COAST = auto()
    OCEAN = auto()

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

        if edges is None: self.edges = []
        else: self.edges = edges

        if corners is None: self.corners = []
        else: self.corners = corners

        self.state = state

    def set_state(self, state: Biomes) -> None:
        """Задает состояние ячейки"""
        if isinstance(state, Biomes):
            self.state = state
        else:
            raise TypeError(f'object {state} is not Biomes(Flag)')

    def add_state(self, state: Biomes) -> None:
        """Добавляет состояние ячейки"""
        if isinstance(state, Biomes):
            self.state = self.state | state
        else:
            raise TypeError(f'object {state} is not Biomes(Flag)')

if __name__ == '__main__':
    print(Biomes.HILL | Biomes.COAST)
    cell = Cell((1, 2), [], [(1, 1), (2, 2)], Biomes.HILL)
    cell.set_state(Biomes.LAKE)
    print(cell.state)
    cell.add_state(Biomes.RIVER)
    cell.add_state(Biomes.ROAD)
    print(cell.state)
