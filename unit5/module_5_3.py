class House:
    def __init__(self, name="ЖК Эльбрус", number_of_floors=30):
        self.name = name
        self.number_of_floors = number_of_floors

    def __len__(self):
        return self.number_of_floors

    def __str__(self):
        return f"Название: {self.name}, кол-во этажей: {self.number_of_floors}"

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

    def go_to(self, new_floor):
        if self.number_of_floors >= new_floor >= 0:
            for floor in range(1, new_floor + 1):
                print(floor)
        else:
            print("Такого этажа не существует")


h1 = House('ЖК Эльбрус', 10)
h2 = House('ЖК Акация', 20)

print(h1)
print(h2)

print(h1 == h2) # __eq__

h1 = h1 + 10 # __add__
print(h1)
print(h1 == h2)

h1 += 10 # __iadd__
print(h1)

h2 = 10 + h2 # __radd__
print(h2)

print(h1 > h2) # __gt__
print(h1 >= h2) # __ge__
print(h1 < h2) # __lt__
print(h1 <= h2) # __le__
print(h1 != h2) # __ne__
