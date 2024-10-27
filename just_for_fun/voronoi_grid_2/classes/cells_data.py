from typing import Type
from queue import Queue
from functools import lru_cache

from just_for_fun.voronoi_grid_2.classes.hexclass import Hex
from just_for_fun.voronoi_grid_2.classes.cellclass import Cell
from just_for_fun.voronoi_grid_2.constants.biomes import Biomes

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
            state: set | Biomes | None = None) -> None:
        """Добавление ячейки в словарь"""
        if node in self.data:  # если ячейка уже была создана...
            cell: Cell = self.data[node]
            # добавление состояния в ячейку
            if state:
                if isinstance(state, Biomes):
                    cell.add_state(state)
                else:
                    cell.add_state(*state)

            # добавление соседей в ячейку
            for edge in edges:
                # если ячейка не была в общем словаре -> добавить
                if edge not in self.data:
                    new_cell: Cell = Cell(edge)
                    self.data[edge] = new_cell
                    self._add_to_search_grid(new_cell)
                cell.add_edges(self.data[edge])

        else:  # создание новой ячейки
            # определение соседей ячейки
            cell_edges = []
            for edge in edges:
                # если ячейка не была в общем словаре -> добавить
                if edge not in self.data:
                    new_cell: Cell = Cell(edge)
                    self.data[edge] = new_cell
                    self._add_to_search_grid(new_cell)
                cell_edges.append(self.data[edge])

            # создание ячейки и добавление ее в словарь
            cell: Cell = Cell(node, cell_edges)
            if state:
                if isinstance(state, Biomes):
                    cell.add_state(state)
                else:
                    cell.add_state(*state)
            self.data[cell.node] = cell
            self._add_to_search_grid(cell)

    def _add_to_search_grid(self, cell: Cell) -> None:
        """Добавление ячейки в словарь для последующего быстрого поиска"""
        # округление координат
        x, y = cell.node[0], cell.node[1]
        x = round(x, 0)
        y = round(y, 0)

        # добавление ячейки в словарь для поиска
        if (x, y) not in self.grid:
            self.grid[(x, y)] = [cell]
        else:
            self.grid[(x, y)].append(cell)

    def nearest_cell(self, coordinate: tuple[float, float]) -> Cell | None:
        """Возвращает ближайшую ячейку"""
        round_coordinate: tuple[int, int] = int(coordinate[0]), int(coordinate[1])

        # список всех ячеек вблизи координат
        cells_around: list[Cell] = []
        for x in range(round_coordinate[0]-1, round_coordinate[0]+2):
            for y in range(round_coordinate[1]-1, round_coordinate[1]+2):
                if (x, y) in self.grid:
                    cells_around.extend(self.grid[(x, y)])

        if len(cells_around) == 0:
            return None
        else:
            return min(cells_around, key=lambda cell: ((cell.node[0] - coordinate[0])**2 +
                                                       (cell.node[1] - coordinate[1])**2))

    #@lru_cache()
    def surroundings(self,
                     cell: Cell,
                     distance: int = 1) -> set[Cell] | None:
        """Возвращает список ячеек вокруг указанной ячейки"""
        if cell is None:
            return set()

        # очередь
        frontier: Queue = Queue()
        step: int = 0
        frontier.put((step, cell))
        # множество найденных ячеек
        reached: set = set()
        reached.add(cell)

        # алгоритм поиска соседей
        while not frontier.empty():
            step, current_cell = frontier.get()
            current_cell: Cell
            if step >= distance:
                break
            for next_cell in current_cell.edges:
                if next_cell not in reached:
                    frontier.put((step+1, next_cell))
                    reached.add(next_cell)

        return reached

    def on_screen(self):
        return self.data.values()

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
    cell_map.add((1.8, 2.4), [], [])
    cell_map.add((2.6, 1.9), [], [])
    cell_map.add((1.9, 1.1), [], [])
    cell_map.add((2.4, 0.55), [], [])
    cell_map.add((0.7, 0.6), [], [])
    cell_map.add((0.3, 1.75), [], [])
    cell_map.add((2.65, 0.8), [], [])
    cell_map2 = CellsMap()
    print("1", cell_map2, "|", cell_map.grid)
    print("2", cell_map2.nearest_cell((1.25, 1.55)))
