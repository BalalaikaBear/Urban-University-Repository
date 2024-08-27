print("1:", type(142))  # int - integer (целое число)
print("2:", type("name"))  # str - string (строка)
print("3:", type(2.0))  # float - (вещественное число)
print("4:", type(True))  # bool - boolean (логический тип данных)
print("5:", type([1, 2]))  # list - список
print("6:", type((1, 2, True)))  # tuple - кортеж
print("7:", type({"a": 1}))  # dict - dictionary (словарь)
print("8:", type({1, 2, 3, 2, "one"}))  # set - множество

print("10:", 42 // 16, 42 / 16)  # // - целочисленное деление, / - деление
print("11:", 7 % 4)  # % - остаток от деления
print("12:", 3 ** 5)  # ** - возведение в степень
print("13:", 6.0 + 11, 120 - 54.96)  # + - сложение, - вычитание

print("14:", "Hello, " + "my friend")  # вычитать строки нельзя
print("15:", '1' + str(5))  # str() - преобразование в строку
print("16:", type(bool("True")))  # bool() - преобразование в boolean

print("20:", 5 >= 10, 11 == 11, 5 != "apple")  # операции с boolean
print("21:", 1 <= 7 and 4 != 5 or not True)

word = "la-li-lu-le-lo"
print("30:", (word + "-")*3 + word[0] + word[-1])  # индексация - вывод указанного символа из строки
print("31:", word[0:9:2])  # вывод символов от 0 до 8 с шагом 2
print("32:", word[:3], word[7:])  # вывод символов от 0 до 2, и от 7 и выше
print("33:", word[::-1])  # вывод символов с шагом -1 (в обратном порядке)
print("34:", len(word))  # количество символов с троке

print("40:", "haHAha".upper())  # преобразовать строку в верхний регистр
print("41:", "haHAha".lower())  # преобразовать строку в нижний регистр
print("42:", "haHAha".replace("HA", "lo"))  # замена заданных символов на новые


# СПИСКИ
food = ["apple", "coconut", "banana"]
food[0] = "peach"  # замена элемента
print("50:", food)
food.append(5)  # добавление элемента в конец
print("51:", food)
food.extend("string")  # добавление символов строки по отдельности
print("52:", food)
food.extend(["string", True])  # добавление списка в конец
print("53:", food)
food.remove("banana")  # удаление элемента
print("54:", food)
print("55:", "coconut" in food)  # проверка наличия элемента в списке
print("56:", "banana" not in food)  # проверка отсутствия элемента


# КОРТЕЖ - неизменяемый список
tuple_1 = 1, 2, "three", 4  # задавать кортеж можно как без скобок
tuple_2 = (1, 2, "three", 4)  # так и с скобками
tuple_3 = tuple(food)  # задания списка в кортеж
print("60:", tuple_1, tuple_2, tuple_3)
print("61:", tuple_3.__sizeof__())  # кортеж занимает меньше памяти чем список
print("62:", food.__sizeof__())
tuple_small = ([1, 4], 10)
tuple_small[0][1] = 2  # замена содержимого к кортеже
print("63:", tuple_small)
print("64:", (1, 2, 3)*5 )  # увеличение количества кортежа в x раз
print("65:", (1, 2) + (6, 7))  # соединение кортежов


# СЛОВАРЬ
phone_book = {"Michel": 88005553535, "Aurora": 88007775533}  # "Michel" - ключ, число - значение
print("70:", phone_book)
print("71:", phone_book["Michel"])  # для обращения к элементу необходимо указать ключ
phone_book["Aurora"] = 89255553636  # замена значения для ключа
print("72:", phone_book)
phone_book["John"] = 84951124545  # при отсутствии указанного ключа, он будет добавлен в словарь
print("73:", phone_book)
 # del
del phone_book["Aurora"]  # удаление ключа
print("74:", phone_book)
 # update
phone_book.update({"Diablo": 65552243737,
                   "Dracula": 59996663322})  # update - добавить в словарь в конец имеющегося словаря
print("75:", phone_book)
 # get
print("76:", phone_book.get("John"))  # получить значение ключа, если нет ключа - None
print("77:", phone_book.get("Alucard", 404))  # при отсутствии необходимого ключа, вернуть указанное значение
 # pop
a = phone_book.pop("Michel")  # метод pop удаляет ключ, но возвращает значение в ключе
print("78:", a, phone_book)
list_1 = [1, 10, 100]
print("79:", list_1.pop(2), list_1)  # метод pop работает также и со списком
 # keys
print("80:", phone_book.keys())  # метод keys возвращает СПИСОК коллекции ключей в словаре
 # values
print("81:", phone_book.values())  # метод values возвращает СПИСОК со значениями в словаре
 # items
print("82:", phone_book.items())  # метод items возвращает целые пары в виде СПИСКА из КОРТЕЖЕЙ


# МНОЖЕСТВА
set_1 = {1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1}
print("90:", set_1)  # множество хранит только уникальные значения
list_1 = [1, 1, 1, 2]
list_1 = set(list_1)  # преобразование списка в множество
print("91:", list_1)
 # discard
set_1.discard(1)  # метод discard удаляет значение
print("92:", set_1)  # discard не выдает ошибку, если элемент не был найден во множестве
 # remove
set_1.remove(6)
print("93:", set_1)
 # add
set_1.add(0)  # метод add добавляет элемент
print("94:", set_1)


# IF
name = "J"
if name == "Mark" or name == "J":
    print("95:", "Oh, hi", name)
else:
    print("95:", "Hello", name)


# WHILE
#while 1 > 0:  # True
#    number = int(input("Введите число:"))
#    if number % 2 == 0:
#        print('Число четное')
#        continue  # пропускает последующие команды и переходит на следующее повторение цикла
#    else:
#        print('Число нечетное')
#        break  # останавливает цикл


# FOR
for i in "hello":  # i возьмет поочередно каждый символ в строке
    print("100:", i)

a = ['one', 'two', 'three']
for i in a:
    print("101:", i)

for i in range(len(a)):  # выведет элементы 0, 1, 2
    print("102:", a[i])  # отобразить i-й элемент

for i in range(1, 11, 3):  # начало последовательности, конец последовательности (не включительно), шаг
    for j in range (1, 11, 4):
        print(f'103: {i} x {j} = {i*j}')

a = {"a": 1, "b": 2, "c": 3}
for i in a:
    print("104:", i, a[i])  # i - ключ, [i] - значение
for i, k in a.items():  # вывод словаря в i и k
    print("105:", i, k)

# name = input("Enter your name: ")  # ввод символов (тип данных - str)


# Встроенные математические функции в Python:
print("110:", round(593.8019101012, 3))  # округляет число; можно указать количество знаков после запятой
max([123, 234, 345, 888])  # возвращает максимальное значение из последовательности
min([123, 234, 345, 888])  # -//- минимальное значение -//-
sum([123, 234, 345, 888])  # сумма значений последовательности
len([123, 234, 345, 888])  # количество элементов в последовательности

numbers = [1000, 2000, 4500, 500, 980]
names = ['Hi', 'Wow', 'UwU', 'Go', 'Yes']
zipped = zip(names, numbers)  # объединение элементов последовательностей по индексам
print("111:", type(zipped), zipped)  # zapped имеет класс zip
print("112:", list(zipped))  # создает список из кортежей
print("113:", dict(zipped), dict(zip(names, numbers)))  # создает словарь; !информация о zipped была удалена из памяти!

a = [True, False, False]
print("115:", any(a))  # если в последовательности есть True, возвращает True; иначе False
print("116:", all(a))  # если все элементы в последовательности True, возвращает True; иначе False
print("117:", dir(a))  # dir() - показать информацию об атрибутах объекта
print("118:", isinstance(a, list))  # isinstance() - соответствие определенному классу
print("119:", type(a) == str)  # аналогично верхней строке
print("120: ID =", id(a))  # id() - уникальный номер переменной (адрес в памяти)


# Ошибки
try:
    for i in [0, 10, 20, "a"]:
        print(10 / i)
except ValueError:
    print(ValueError)
except ZeroDivisionError as exc:  # сохранения объекта ошибки в переменную
    print("130:", type(exc), exc)
except:
    print("pass")
else:  # выполняется если ошибки не было
    pass
finally:  # дополнительный код, выполняющийся в конце
    pass

def greet_person(name):
    if name == "Заяц":
        try:
            raise Exception("Проезд зайцам воспрещен!")  # raise <Класс ошибки> (<аргумент ошибки>) - генерирование собственного исключения
            raise  # можно вызывать raise без указания класса
        except Exception as exc:
            print("130.b:", type(exc), exc)  # при выводе объекта Exception выводится ранее записанный аргумент
    else:
        print(f"130.a: Привет, {name}!")
greet_person("Волк")
greet_person("Заяц")

class ProZero(Exception):  # собственный класс ошибки, наследуемый от Exception
    def __init__(self, message, extra_info):
        self.message = message
        self.extra_info = extra_info
def f(a, b):
    if b == 0:
        raise ProZero("Деление на ноль невозможно", {"a": a, "b": b})  # вызов собственного класса ошибки, работает только при указании атрибута
    return a / b
try:
    print(f(5, 0))
except ProZero as e:
    print("131:", e.message, e.extra_info)


# ФУНКЦИОНАЛЬНОЕ ПРОГРАМИРОВАНИЕ
numbers = (4, 2, 1, 4, 7, 12)
# map применяет функцию к каждому элементу последовательности и формирует список результатов
result = map(lambda x: x*2, numbers)  # result является объектом функции
print("140:", result, type(result), list(result))

# filter вычисляет функцию для каждого аргумента и добавляет элемент в список результатов, если только функция вернула True
result = filter(lambda x: x%2, numbers)
print("141:", list(result))

# генерация списков (списковая сборка) / аналог map
list_comp_1 = [x*2 for x in numbers]
print("142:", list_comp_1)

# генерация списков с фильтрацией
# выполняет фильтрацию по условию x > 5, затем выполняет код x*2
list_comp_2 = [x*2 for x in numbers if x > 5]
print("143:", list_comp_2)

# генерация списков, изменение операции над элементом
# выполняет определенный код исходя из условий
list_comp_3 = [x/2 if x>2 else x*10 for x in numbers]
print("144:", list_comp_3)

# генерация списков для двух элементов
numbers_2 = [3, 4, 5]
list_comp_4 = [x*y for x in numbers for y in numbers_2]
print("145:", list_comp_4)
list_comp_5 = [x*y for x in numbers for y in numbers_2 if x%2 and y//2]
print("146:", list_comp_5)

# генерация множества и словаря
result = {x for x in numbers}
result_2 = {x: x**2 for x in numbers}
print("147:", result, result_2)

# генераторные сборки (ленивые вычисления)
# значения вычисляются при вызове функции/генератора. Генератор можно использовать только ОДИН РАЗ!
# работает быстрее генератора списков. Имеется в range(), zip(), open(), map()
result = (x**100 for x in numbers)
print("148:", result, type(result))
for elem in result:
    print("148.a:", elem)

# анонимная функция lambda, она имеет ограниченное применение:
# - она создается в процессе выполнения кода (а не при компиляции) и может просадить быстродействие
# - она плохо сериализуется - могут быть проблемы в крупных фреймворках
# - лямбда функция не имеет имени, т.е. на нее нельзя ссылаться
my_func = lambda x: x+10
print("150:", my_func, type(my_func), list(map(my_func, numbers)), my_func.__name__)

# создание функции внутри функции
def get_multiplier_v1(n):  # get_multiplier_v1 - функция высшего порядка, она возвращает функции
    if n == 2:
        def multiplier(x):
            return x * 2

    elif n == 3:
        def multiplier(x):
            return x * 3

    else:
        raise Exception("Я могу только умножать на 2 или 3!")

    return multiplier

by_2 = get_multiplier_v1(2)
by_3 = get_multiplier_v1(3)

print("151:", list(map(by_2, numbers)))
print("151.1:", list(map(by_3, numbers)))

def get_multiplier_v2(n):
    def multiplier(x):
        return x * n
    return multiplier

by_5 = get_multiplier_v2(5)
print("153:", by_5(x=42))  # 42 * 5

by_10 = get_multiplier_v2(10)
by_100 = get_multiplier_v2(100)
print("153.1", list(map(by_10, numbers)))
print("153.2", list(map(by_100, numbers)))

# пример создания матрицы
def matrix(some_list):
    def multiply_column(x):
        res = []
        for element in some_list:
            res.append(element * x)
        return res
    return multiply_column

print(list(map(matrix(numbers), numbers_2)))

# создание объекта, который можно вызвать
class Multiplier:
    def __init__(self, n):
        self.n = n
    def __call__(self, x):
        # если есть такой метод у класса, то его объект можно вызывать как функцию
        return x * self.n

by_101 = Multiplier(101)
print("154:", by_101(5))  # 5 * 100
print("154.1:", list(map(by_101, numbers)))

# Итераторы
# __iter__(self) - получение итератора для перебора объекта
# __next__(self) - переход к следующему значению и его считывание
class Iter:
    def __init__(self):
        self.first = "Первый элемент"
        self.second = "Второй элемент"
        self.third = "Третий элемент"
        self.i = 0

    def __iter__(self):
        # обнуляем счетчик перед циклом
        self.i = 0
        # возвращаем ссылку на себя, т.к. сам объект должен быть итератором
        return self

    def __next__(self):
        # этот метод возвращает значения по требованию python (ленивые вычисления)
        self.i += 1
        if self.i == 1:
            return self.first
        elif self.i == 2:
            return self.second
        elif self.i == 3:
            return self.third
        elif self.i == 4:
            return "Подсчет закончен"
        raise StopIteration()  # признак того, что больше возвращать нечего

for value in Iter():        # интерпретатор вызывает метод __next__ при каждом проходе цикла
    print("160.a:", value)  # если в __next__ возникает исключение StopIteration - значит в объекте больше нет элементов - цикл прекращается

obj = Iter()
try:  # представление цикла for через исключение StopIteration
    while True:
        value = obj.__next__()
        print("160.b:", value)
except StopIteration:
    print("160.b: Цикл for закончен")

# числа Фибоначчи
def fibonacci(n):
    result = []
    a, b = 0, 1
    for _ in range(n):
        result.append(a)
        a, b = b, a+b
    return result

print("161:", end=" ")
for value in fibonacci(n=10):
    print(value, end=" ")

class Fibonacci:
    def __init__(self, n):
        self.i, self.a, self.b, self.n = 0, 0, 1, n
    def __iter__(self):
        self.i, self.a, self.b = 0, 0, 1
        return self
    def __next__(self):
        self.i += 1
        if self.i > 1:
            if self.i > self.n:
                raise StopIteration
            self.a, self.b = self.b, self.a + self.b
        return self.a

print("\n162:", end=" ")
for value in Fibonacci(30):
    print(value, end=" ")
