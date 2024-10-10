from collections import namedtuple
from collections.abc import Iterable
from enum import Flag, auto
from typing import Callable

class Bioms:
    def __init__(self, *bioms: tuple['Biom']):
        pass

class Biom(Flag):
    GRASSLAND = auto()
    DESERT = auto()
    SAVANNA = auto()
    FOREST = auto()
    TUNDRA = auto()
    TAIGA = auto()
    MOUNTAIN = auto()
    HILL = auto()
    RIVER = auto()
    LAKE = auto()
    COAST = auto()
    OCEAN = auto()

    def set(self, value):
        self.value = value.value

    def add(self, value):
        self.value += value.value

class Cell(namedtuple(typename='Cell',
                      field_names=['node', 'edges', 'corners', 'state'])):
    node: tuple[float, float]
    edges: list['Cell']
    corners: tuple[tuple[float, float]]
    state: Biom
    __slots__ = ()

print(Biom.HILL | Biom.COAST)
cell = Cell((1, 2), [], ((1, 1), (2, 2)), Biom.HILL)
print(id(cell), cell)
cell.edges.append(3)
print(id(cell), cell)
print(dir(Biom))
cell.state.set(Biom.OCEAN)
cell.state.add(Biom.LAKE)
print(dir(Biom))
print(id(cell), cell.state)
print(cell.state.value)
