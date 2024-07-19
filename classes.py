class Human:  # создание собственного типа данных
    def __init__(self, name="47"):  # инициализатор (конструктор класса) - что будет создаваться при инициализации объекта
        self.name = name  # задание собственной переменной

man = Human("Alukard")  # создание переменной типа класс
woman = Human(name="Wednesday")
forty_seven = Human()  # скобки ОБЯЗАТЕЛЬНЫ!

print("1:", type(man))  # собственный тип данных
print("2:", man == woman, man is woman, id(man), id(woman))  # каждый объект из класса уникальный
print("3:", man.name, forty_seven.name)  # обращение к данным