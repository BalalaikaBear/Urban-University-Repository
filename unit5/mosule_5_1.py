class House():
    def __init__(self, name="ЖК Эльбрус", number_of_floors=30):
        self.name = name
        self.number_of_floors = number_of_floors

    def go_to(self, new_floor):
        if new_floor <= self.number_of_floors and new_floor >= 0:
            print(new_floor)
        else:
            print("Такого этажа не существует")

first = House("Хижина в лесу", 3)

first.go_to(4)
first.go_to(1)
first.go_to(-1)