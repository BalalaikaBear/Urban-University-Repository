from typing import Self, Type

from cellclass import Cell
from hexclass import Hex
from chunks import CHUNK_SIZE

class CellsMap:
    __instance = None

    def __new__(cls) -> Type['CellsMap']:  # паттерн Singleton - объект класса создается единожды
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)  # чтобы избежать повторной инициализации
        return cls.__instance

    def __init__(self) -> None:
        self.data: dict[Hex: dict[tuple[float, float]: Cell]] = \
            {Hex(0, 0): {(0, 41): Cell((0, 41))},
             Hex(1, 0): {(0.2, 0.0003): Cell((0.2, 0.0003)),
                         (13.21, 1.3): Cell((13.21, 1.3))}}

    def add(self, item: Cell):
        """Добавление ячейки в словарь"""
        self.__iadd__(item)

    def __iadd__(self, other: Cell):
        """Добавление ячейки в словарь через оператор +="""
        if not isinstance(other, Cell):
            raise TypeError(f"в словарь можно добавить только объект класса 'Cell'")
        self.data[Cell.chunk][Cell.node] = other

    def __getitem__(self, item):
        """CellsMap[coord] -> Cell"""
        pass

    def __setitem__(self, key, value):
        """CellsMap[key/coord] = Cell -> добавляет ячейку в словарь"""
        pass

    def __contains__(self, item: Cell | tuple[float, float]) -> bool:
        """Поиск по позиции ячейки"""
        if isinstance(item, Cell):
            item = item.node
        for data_chunk in self.data.values():
            if item in data_chunk:
                return True
        return False

    def __len__(self) -> int:
        """Возвращает количество элементов в словаре"""
        return sum((len(chunk) for chunk in self.data.values()))

    def __str__(self) -> str:
        size = len(self)
        if size <= 1:
            return f'{self.__class__.__name__}({size} cell)'
        else:
            return f'{self.__class__.__name__}({size} cells)'

if __name__ == '__main__':
    cell_map = CellsMap()
    print((0, 41) in cell_map)
    cell_map += Cell((0.01, 42))
    print(cell_map)
