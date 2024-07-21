class House:
    def __init__(self, name="ЖК Эльбрус", number_of_floors=30):
        self.name = name
        self.number_of_floors = number_of_floors

    def __len__(self):
        return self.number_of_floors

    def __str__(self):
        return f"Название: {self.name}, кол-во этажей: {self.number_of_floors}"

    def go_to(self, new_floor):
        if self.number_of_floors >= new_floor >= 0:
            for floor in range(1, new_floor + 1):
                print(floor)
        else:
            print("Такого этажа не существует")


h1 = House('ЖК Эльбрус', 10)
h2 = House('ЖК Акация', 20)

print(str(h1))
print(str(h2))

print(len(h1))
print(len(h2))
