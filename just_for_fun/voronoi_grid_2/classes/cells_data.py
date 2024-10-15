from typing import Type

from hexclass import Hex
from cellclass import Cell

class CellsMap:
    __instance = None
    __slots__ = ['data', 'grid']

    def __new__(cls, *args, **kwargs) -> Type['CellsMap']:  # паттерн Singleton - объект класса создается единожды
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        if not hasattr(self, 'data'):  # предотвращение повторной инициализации
            self.data: dict[Hex: Cell] = \
                    {(0, 41): Cell((0, 41)),
                     (0.2, 0.0003): Cell((0.2, 0.0003)),
                     (13.21, 1.3): Cell((13.21, 1.3))}
            self.grid: dict[tuple[int, int]: list[Cell]] = {(0, 0): [Cell((0.2, 0.0003))]}

    def add(self, item: Cell):
        """Добавление ячейки в словарь"""
        if not isinstance(item, Cell):
            raise TypeError(f"в словарь можно добавить только объект класса 'Cell'")

        # добавление или замена объекта в общем словаре
        self.data[item.node] = item

        # добавление объекта в словарь для быстрого поиска ячейки рядом
        x, y = item.node[0], item.node[1]
        x = int(x) if x > 0 else int(x)-1
        y = int(y) if y > 0 else int(y)-1
        if (x, y) not in self.grid:
            self.grid[(x, y)] = [item]
        else:
            self.grid[(x, y)].append(item)

    def __getitem__(self, item):
        """CellsMap[coord] -> Cell"""
        return self.data[item]

    def __setitem__(self, key, value):
        """CellsMap[key/coord] = Cell -> добавляет ячейку в словарь"""
        self.data[key] = value

    def __contains__(self, item: Cell | tuple[float, float]) -> bool:
        """Поиск по позиции ячейки"""
        if isinstance(item, Cell):
            item = item.node
        return item in self.data

    def __len__(self) -> int:
        """Возвращает количество элементов в словаре"""
        return len(self.data)

    def __str__(self) -> str:
        size = len(self.data)
        if size <= 1:
            return f'{self.__class__.__name__}({size} cell)'
        else:
            return f'{self.__class__.__name__}({size} cells)'

if __name__ == '__main__':
    cell_map = CellsMap()
    cell_map.add(Cell((0.12, 0.2)))
    cell_map2 = CellsMap()
    print(cell_map.grid)
