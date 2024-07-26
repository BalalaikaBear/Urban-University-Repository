class Human:  # создание собственного типа данных

    head = True # общий атрибут

    def __init__(self, name="47", age=0):  # инициализатор (конструктор класса) - что будет создаваться при инициализации объекта
        self.name = name  # задание собственной переменной
        self.age = age
#       self.say_info() - вызов функции при создании класса

    def __del__(self):  # деструктор - срабатывает при удалении объекта из памяти (при ЗАВЕРШЕНИИ программы также СРАБАТЫВАЕТ!)
        print(f"__del__: {self.name} ушёл")

    def __len__(self):  # при вызове функции len будет возвращаться возраст объекта
        return self.age

    def __str__(self):  # возвращает строковое представление нашего объекта
        return f"Имя: {self.name}, возраст: {self.age} "

    # перезаписывание стандартных boolean операторов
    def __lt__(self, other):  # "less than"
        return self.age < other.age

    def __gt__(self, other):  # "greater than"
        return self.age > other.age

    def __eq__(self, other):  # "equal"
        return self.age == other.age

    def __le__(self, other):  # "less equal"
        return self.age <= other.age

    def __ge__(self, other):  # "greater equal"
        return self.age >= other.age

    def __ne__(self, other):  # "not equal"
        return self.age != other.age

    def __bool__(self):  # переопределение метода bool
        return bool(self.name)

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
print("6:", man > woman)  # обращение к функции __lt__ в классах - сравнение объектов
print("7:", woman)  # возвращается текст из функции __str__ в классе

man.say_info()  # вызов метода для определенного класса


class User:
    __instance = None
    def __new__(cls, *args, **kwargs):  # __new__ ссылается к классу. Срабатывает перед созданием объекта класса
        print("10:", "__new__")
        # если не был создан ни один объект этого класса, то в __instance записывается ссылка на наш класс.
        # Метод __new__ возвращает саму ссылку на наш класс.
        if cls.__instance is None:                         # паттерн Singleton - объект класса создается единожды,
            cls.__instance = super().__new__(cls)          # чтобы избежать повторной его инициализации
        return cls.__instance  # метод __new__ ДОЛЖЕН возвращать ссылку на класс

    def __init__(self, *args, **kwargs):  # __init__ ссылается к объекту. Срабатывает после создания класса объекта
        print("11:", "__init__")
        self.args = args
        for key, values in kwargs.items():  # задание собственных атрибутов из входящих данных в **kwargs
            setattr(self, key, values)

    # self - указатель на объект класса
    # cls - указатель на класс

other = [1, 2, 3]
user = {"name": "Karl", "age": 20}

user1 = User(*other, **user)
user2 = User(*[1, 3, 5], **user)
print("12:", user1 is user2, id(user1), id(user2))  # переменные занимают ту же ячейку памяти
print("13:", user1.args, user2.name)
