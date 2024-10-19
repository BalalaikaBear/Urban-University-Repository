from typing import Type

from just_for_fun.voronoi_grid_2.classes.hexclass import Hex
from just_for_fun.voronoi_grid_2.classes.cellclass import Cell

class CellsMap:
    __instance = None
    __slots__ = ['data', 'grid']

    def __new__(cls, *args, **kwargs) -> Type['CellsMap']:  # паттерн Singleton - объект класса создается единожды
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        if not hasattr(self, 'data'):  # предотвращение повторной инициализации
            self.data: dict[tuple[float, float]: Cell] = {}
            self.grid: dict[tuple[int, int]: list[Cell]] = {}

    def add(self,
            node: tuple[float, float],
            edges: list[tuple[float, float]],
            corners: list[tuple[float, float]]) -> None:
        """Добавление ячейки в словарь"""
        if node in self.data:
            cell: Cell = self.data[node]

            # добавление соседей в ячейку
            for edge in edges:
                # если ячейка не была в общем словаре -> добавить
                if edge not in self.data:
                    new_cell: Cell = Cell(edge)
                    self.data[edge] = new_cell
                    self._add_to_search_grid(new_cell)
                cell.add_edges(self.data[edge])

            # добавление границ ячейки
            cell.add_corners(*corners)

        else:
            # определение соседей ячейки
            cell_edges = []
            for edge in edges:
                if edge in self.data:
                    cell_edges.append(self.data[edge])
                else:
                    cell_edges.append(edge)

            # создание ячейки и добавление ее в словарь
            cell: Cell = Cell(node, cell_edges, corners)
            self.data[cell.node] = cell
            self._add_to_search_grid(cell)

    def _add_to_search_grid(self, cell: Cell) -> None:
        """Добавление ячейки в словарь для последующего быстрого поиска"""
        # округление координат
        x, y = cell.node[0], cell.node[1]
        x = int(x) if x > 0 else int(x) - 1
        y = int(y) if y > 0 else int(y) - 1

        # добавление ячейки в словарь для поиска
        if (x, y) not in self.grid:
            self.grid[(x, y)] = [cell]
        else:
            self.grid[(x, y)].append(cell)

    def nears_cell_coord(self) -> tuple[float, float]:
        """Возвращает координаты ближайшей ячейки"""
        pass

    def __getitem__(self, item: tuple[float, float]) -> Cell:
        """CellsMap[coord] -> Cell"""
        return self.data[item]

    def __setitem__(self, key: tuple[float, float], value: Cell) -> None:
        """CellsMap[key/coord] = Cell -> добавляет ячейку в словарь"""
        self.data[key] = value
        self._add_to_search_grid(value)

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
    #cell_map.add(Cell((0.12, 0.2)))
    cell_map2 = CellsMap()
    print(cell_map.grid)
