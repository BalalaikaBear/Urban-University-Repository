class House:
    houses_history = []  # классовый атрибут, хранит названия созданных объектов

    # ----------------------------
    # СПЕЦИАЛЬНЫЕ МЕТОДЫ

    def __new__(cls, *args, **kwargs):  # записывание названия созданного объекта в атрибут houses_history
        cls.houses_history.append(args[0])
        return object.__new__(cls)

    def __init__(self, name="ЖК Эльбрус", number_of_floors=30):
        self.name = name
        self.number_of_floors = number_of_floors

    def __del__(self):
        print(f"{self.name} снесён, но он останется в истории")

    # ----------------------------
    # МАГИЧЕСКИЕ МЕТОДЫ

    def __len__(self):
        return self.number_of_floors

    def __str__(self):
        return f"Название: {self.name}, кол-во этажей: {self.number_of_floors}"

    # ----------------------------
    # ПЕРЕГРУЗКА ОПЕРАТОРОВ

    def __eq__(self, other):  # "equal"
        return self.number_of_floors == other.number_of_floors

    def __ne__(self, other):  # "not equal"
        return self.number_of_floors != other.number_of_floors

    def __lt__(self, other):  # "less than"
        return self.number_of_floors < other.number_of_floors

    def __gt__(self, other):  # "greater than"
        return self.number_of_floors > other.number_of_floors

    def __le__(self, other):  # less equal"
        return self.number_of_floors <= other.number_of_floors

    def __ge__(self, other):  # greater equal"
        return self.number_of_floors >= other.number_of_floors

    def __add__(self, value):  # self + value
        if isinstance(value, int):
            return House(number_of_floors=self.number_of_floors + value)

    def __radd__(self, value):  # value + self
        return self.__add__(value)

    def __iadd__(self, value):  # +=
        return self.__add__(value)

    # ----------------------------
    # ФУНКЦИИ

    def go_to(self, new_floor):
        if self.number_of_floors >= new_floor >= 0:
            for floor in range(1, new_floor + 1):
                print(floor)
        else:
            print("Такого этажа не существует")


h1 = House('ЖК Эльбрус', 10)
print(House.houses_history)
h2 = House('ЖК Акация', 20)
print(House.houses_history)
h3 = House('ЖК Матрёшки', 20)
print(House.houses_history)

# Удаление объектов
del h2
del h3

print(House.houses_history)

