from typing import Optional, Any
from numbers import Real  # real numbers as a type
from collections.abc import MutableMapping

# Сокращение записи типов объектов
type Hex[q, r] = tuple[Real, Real]

class Map(MutableMapping):
    """Содержит информацию о карте в виде словаря"""
    def __init__(self, data: Optional[dict[Hex, Any]] = None) -> None:
        if data is None:
            self.data = {}
        else:
            self.data = data

    def cells_around(self, center: Hex, *, radius: int = 1) -> set[Hex]:
        """
        Возвращает множество ячеек, вокруг указанной ячейки

        :param center: Положение ячейки в координатах [q, r]
        :param radius: Радиус поиска ячеек вокруг
        :return: Множество ячеек
        """
        return set((q + center[0], r + center[1])
                   for q in range(-radius, radius + 1)
                   for r in range(max(-radius, -q-radius), min(radius, -q+radius) + 1)
                   if (q + center[0], r + center[1]) in self)

    def __getitem__(self, item: Any) -> Any:
        return self[item]

    def __setitem__(self, key: Hex, value: Any) -> None:
        self.data[key] = value

    def __delitem__(self, key: Hex) -> None:
        del self.data[key]

    def __iter__(self) -> iter:
        return iter(self.data)

    def __len__(self) -> int:
        return len(self.data)

    def __str__(self) -> str:
        return f'Size of a map is {self.__len__} items'



