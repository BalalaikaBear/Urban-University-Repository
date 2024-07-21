class Human:  # создание собственного типа данных
    def __init__(self, name="47", age=0):  # инициализатор (конструктор класса) - что будет создаваться при инициализации объекта
        self.name = name  # задание собственной переменной
        self.age = age
#       self.say_info() - вызов функции при создании класса

    def __del__(self):  # деструктор - срабатывает при удалении объекта из памяти (при ЗАВЕРШЕНИИ программы также СРАБАТЫВАЕТ!)
        print(f"__del__: {self.name} ушёл")

    def __len__(self):  # при вызове функции len будет возвращаться возраст объекта
        return self.age

    def say_info(self):  # создание метода в классе
        print(f"Привет, меня зовут {self.name}, мне {self.age}")

man = Human("Alukard", 665)  # создание переменной типа класс
woman = Human(name="Wednesday", age=11)
woman.surname = "Friday"  # задание атрибута для объекта (атрибут не был создан заранее
forty_seven = Human()  # скобки ОБЯЗАТЕЛЬНЫ!

print("1:", type(man))  # собственный тип данных
print("2:", man == woman, man is woman, id(man), id(woman))  # каждый объект из класса уникальный
print("3:", type(woman.__getstate__()), woman.__getstate__())  # отображение всех атрибутов класса в виде словаря
print("4:", man.name, forty_seven.name)  # обращение к данным
print("5:", len(man))  # обращение к функции __len__ в классе

man.say_info()  # вызов метода для определенного класса