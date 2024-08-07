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
