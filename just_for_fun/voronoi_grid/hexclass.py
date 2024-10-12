import pygame
from collections.abc import Iterable
from typing import Callable

_round: Callable = round

class Hex:
    __slots__ = ['q', 'r']

    # Кортеж из положений соседних ячеек по часовой стрелке
    HEX_DIRECTIONS: tuple = ((1, -1), (1, 0), (0, 1),
                             (-1, 1), (-1, 0), (0, -1))

    __objects = {}  # словарь с уже созданными объектами данного класса

    def __new__(cls, q, r) -> 'Hex':
        """Ограничение на создание одинаковых объектов"""
        key = (q, r)  # создание объекта с координатами
        if key in cls.__objects:  # если объект уже был создан - возвращает его
            return cls.__objects[key]  # метод __new__ ДОЛЖЕН возвращать ссылку на класс
        else:
            obj = super().__new__(cls)  # избегание повторной инициализации
            cls.__objects[key] = obj  # добавление нового объекта в словарь созданных объектов
            return obj  # метод __new__ ДОЛЖЕН возвращать ссылку на класс

    def __init__(self, q, r) -> None:
        self.q = q
        self.r = r

    @property
    def s(self) -> 'Hex':
        """Возвращает координату s"""
        return -self.q - self.r

    def distance(self, hexagon) -> int:
        """Расстояние между двумя ячейками"""
        if isinstance(hexagon, Hex):
            return len(self - hexagon)
        else:
            raise TypeError('invalid type')

    def direction(self, direct: int | str) -> tuple[float, float]:
        """Возвращает ячейку в зависимости от введенного направления"""
        if direct in [1, 2, 3, 4, 5, 6]:
            return self.HEX_DIRECTIONS[direct-1]
        elif direct == 'n' or direct == 'north':
            return self.HEX_DIRECTIONS[5]
        elif direct == 'ne' or direct == 'north-east':
            return self.HEX_DIRECTIONS[0]
        elif direct == 'se' or direct == 'south-east':
            return self.HEX_DIRECTIONS[1]
        elif direct == 's' or direct == 'south':
            return self.HEX_DIRECTIONS[2]
        elif direct == 'sw' or direct == 'south-west':
            return self.HEX_DIRECTIONS[3]
        elif direct == 'nw' or direct == 'north-west':
            return self.HEX_DIRECTIONS[4]

    def neighbor(self, direct: int, *, dist: int = 1) -> 'Hex':
        """Возвращает следующую ячейку по направлению"""
        if dist == 1:
            new_hex = self + self.direction(direct)
            return Hex(new_hex.q, new_hex.r)
        else:
            new_hex = Hex(self.q, self.r)
            for _ in range(dist):
                new_hex = new_hex + self.direction(direct)
            return new_hex

    def neighbors(self) -> tuple['Hex', ...]:
        list_of_hexes = []
        for direct in range(1, 7):
            list_of_hexes.append(self.neighbor(direct))
        return tuple(list_of_hexes)

    def round(self) -> 'Hex':
        """Возвращает ближайшую ячейку к точке"""
        q = int(_round(self.q))
        r = int(_round(self.r))
        s = int(_round(-self.q - self.r))
        q_diff = abs(q - self.q)
        r_diff = abs(r - self.r)
        s_diff = abs(s + self.q + self.r)
        if q_diff > r_diff and q_diff > s_diff:
            q = -r - s
        elif r_diff > s_diff:
            r = -q - s
        # else:
        #    s = -q - r
        return Hex(q, r)

    def __add__(self, other: float | Iterable) -> 'Hex':
        """Сложение координат ячеек"""
        # число
        if isinstance(other, (int, float)):
            return Hex(self.q + other, self.r + other)
        # массив
        elif isinstance(other, Iterable) and not isinstance(other, str):
            return Hex(self.q + other[0], self.r + other[1])
        else:
            raise TypeError(f"invalid type")

    def __sub__(self, other: float | Iterable) -> 'Hex':
        """Вычитание координат ячеек"""
        # число
        if isinstance(other, (int, float)):
            return Hex(self.q - other, self.r - other)
        # массив
        elif isinstance(other, Iterable) and not isinstance(other, str):
            return Hex(self.q - other[0], self.r - other[1])
        else:
            raise TypeError(f"invalid type")

    def __mul__(self, other: float | Iterable) -> 'Hex':
        """Умножение координат ячеек"""
        # число
        if isinstance(other, (int, float)):
            return Hex(self.q * other, self.r * other)
        # массив
        elif isinstance(other, Iterable) and not isinstance(other, str):
            return Hex(self.q * other[0], self.r * other[1])
        else:
            raise TypeError(f"invalid type")

    def __truediv__(self, other: float) -> 'Hex':
        # число
        if isinstance(other, (int, float)):
            return Hex(self.q / other, self.r / other)
        else:
            raise TypeError(f"invalid type")

    def __floordiv__(self, other: float) -> 'Hex':
        # число
        if isinstance(other, (int, float)):
            return Hex(self.q // other, self.r // other)
        else:
            raise TypeError(f"invalid type")

    def __mod__(self, other: float) -> 'Hex':
        # число
        if isinstance(other, (int, float)):
            return Hex(self.q % other, self.r % other)
        else:
            raise TypeError(f"invalid type")

    def __getitem__(self, item: int | str) -> float:
        if item == 0 or item == 'q':
            return self.q
        elif item == 1 or item == -1 or item == 'r':
            return self.r

    def __len__(self) -> int:
        """Расстояние до ячейки"""
        return int((abs(self.q) + abs(self.r)) / 2)

    def __str__(self) -> str:
        return f'({self.q}, {self.r})'

    def __repr__(self) -> str:
        return f'Hex({self.q}, {self.r})'


if __name__ == '__main__':
    hex_vector = Hex(4, 3)
    #d = {hex_vector: 'info'}
    #print(d)
    #print(hex_vector + pygame.Vector2(10, 1))
    #print(pygame.Vector2(2, 2) * pygame.Vector2(3, 6))
    #print(hex_vector.neighbor(3, dist=2))
    print(hex_vector.neighbors())
    #print(Hex(10, 2).s)
    #print(len(hex_vector))
    #print(dir(hex_vector))
