import math


class Figure:
    def __init__(self, color, *sides, sides_count=0):
        self.sides_count = sides_count  # количество сторон
        self.__sides_create(sides)  # заполнение атрибута __sides
        self.__color = tuple(color)  # цвет фигуры
        self.filled = True  # фигура заполненная или полая?

    def get_color(self):
        """
        Вернуть цвет фигуры
        """
        return self.__color

    def __is_valid_color(self, r, g, b):
        """
        Проверка на верное заполнение атрибута __color
        """
        if r in range(256) and g in range(256) and b in range(256):
            return True
        else:
            return False

    def set_color(self, r, g, b):
        """
        Задать новый цвет фигуры
        """
        if self.__is_valid_color(r, g, b):
            self.__color = (r, g, b)

    def __is_valid_sides(self, sides):
        """
        Проверка на верное заполнение значений в атрибуте __sides
        """
        try:
            if len(sides) == self.sides_count:

                check = 0
                for side in sides:
                    if side >= 0:
                        check += 1

                if check == self.sides_count:
                    return True
                else:
                    return False

            else:
                return False

        except ValueError:  # если не int, float
            return False

    def get_sides(self):
        """
        Вернуть длины сторон фигуры
        """
        return list(self.__sides)

    def __len__(self):
        """
        Возвращает периметр фигуры
        """
        perimeter = 0
        for side in self.__sides:
            perimeter += side
        return perimeter

    def set_sides(self, *new_sides):
        """
        Задать новые длины сторон фигуры
        """
        if len(new_sides) == self.sides_count and self.__is_valid_sides(new_sides):
            self.__sides = new_sides

    def __sides_create(self, sides):
        """
        Создание атрибута __sides
        """
        if len(sides) == self.sides_count and self.__is_valid_sides(sides):
            self.__sides = sides
        else:
            if len(sides) == 1:  # если указана длина только одной стороны -> продублировать необходимое количество раз
                self.__sides = tuple([sides[0] for x in range(self.sides_count)])
            else:  # если количество указанных длин не соответствует фигуре -> принять все стороны = 1
                self.__sides = tuple([1 for x in range(self.sides_count)])


class Circle(Figure):
    def __init__(self, color, *sides, sides_count=1):
        super().__init__(color, *sides, sides_count=sides_count)
        self.__radius = self._Figure__sides[0] / 2 * math.pi  # радиус круга

    def get_square(self):
        """
        Площадь круга
        """
        return math.pi * self.__radius * self.__radius


class Triangle(Figure):
    def __init__(self, color, *sides, sides_count=3):
        super().__init__(color, *sides, sides_count=sides_count)
        self.__height = 2*self.get_square() / self._Figure__sides[0]

    def get_square(self):
        """
        Площадь треугольника по формуле Герона
        """
        half_p = self.__len__() / 2
        return math.sqrt(half_p * (half_p - self._Figure__sides[0])
                         * (half_p - self._Figure__sides[1])
                         * (half_p - self._Figure__sides[2]))


class Cube(Figure):
    def __init__(self, color, *sides, sides_count=12):
        super().__init__(color, *sides, sides_count=sides_count)
        self.__sides = [self._Figure__sides[0]] * self.sides_count  # лишняя строка, но задание требует ее написать

    def get_volume(self):
        """
        Объём куба
        """
        return self.__sides[0] ** 3  # можно обращаться к атрибуту класса Figure


circle1 = Circle((200, 200, 100), 10, 2) # (Цвет, стороны)
cube1 = Cube((222, 35, 130), 6)

# Проверка на изменение цветов:
circle1.set_color(55, 66, 77) # Изменится
print(circle1.get_color())
cube1.set_color(300, 70, 15) # Не изменится
print(cube1.get_color())

# Проверка на изменение сторон:
cube1.set_sides(5, 3, 12, 4, 5) # Не изменится
print(cube1.get_sides())
circle1.set_sides(15) # Изменится
print(circle1.get_sides())

# Проверка периметра (круга), это и есть длина:
print(len(circle1))

# Проверка объёма (куба):
print(cube1.get_volume())
