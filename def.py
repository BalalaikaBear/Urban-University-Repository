import random

def say_hello(user = "Admin"):  # def <название функции> (<локальные данные>)  <user = ""> - значение по умолчанию
    print(f'Hello {user}')
say_hello()
say_hello("Arnold")
say_hello("Mark")

def lottery():  # возвращающая функция
    tickets = [1,2,3,4,5,6,7,8,9]
    win = random.choice(tickets)
    return win  # останавливает выполнение функции
    print("Alarm!")
print(lottery())

def lottery2(*args, **kwargs):  # *<название переменной> - несколько значений
    tickets = [1,2,3,4,5,6,7,8,9]
    win = random.choice(tickets)
    print(*args)
    return win
print(lottery2(1,2,3,4,5,6,))

def test(a = 2, b = True):  # принимающая функция
    print(a, b)
test(*[1, 2])  # * - распаковка списка (распаковка позиционных параметров)
               # ** распаковка именованных параметров (словарь)

def printer():
    global a, b  # возможность перезаписывания глобальных имен
    a = True
    b = False
    print(a, b)
a = 10
b = 15
print(a, b)
printer()

def print_params(a, *, b, c):  # позле * аргументы необходимо прописывать при вызове функции
    print(a, b, c)
print_params(1, b=True, c="Hi")

def print_params2(*params):
    print(params)  #-> кортеж (1, 2, 3, 4, 5, 6, 7)
    print(*params)  #-> 1, 2, 3, 4, 5, 6, 7  распаковка кортежа
print_params2(1, 2, 3, 4, 5, 6, 7, 8)  # упаковка кортежа

def print_params3(a, b, c):
    print(a, b, c)
list_ = [10, 20, 30]
print_params3(*list_)  # * - распаковка списка

dict_ = {"a": 1, "b": 2, "c": 3}
print_params3(**dict_)  # ** - распаковка словаря. Имена ключей должны соответствовать именам параметров

print()

def summator(*values):
    s = 0
    for i in values:
        s += i
    return s
print("sum =", summator(1, 2, 3, 4, 5, 6, 7))

def info(song, *types, name="John", **values):  # * неименованные параметры, ** именованные параметры
    print("Аргумент:", values)  # -> словарь
    for key, value in values.items():
        print(key, value)
    print(types)
info("Poets", 1,2,3,4, name="Karl", course="Python", date="2022-02-12")

print()

def print_list(a = 3, b = []):  # список b был создан в момент определения функции
    b.append(a)
    print(b)
print_list()
print_list(5)
print_list(10)

def print_list2(a = 3, b = None):
    if b is None:  # исправление накапливания списка
        b = []
    b.append(a)
    print(b)
print_list2(b=[-1])
print_list2(5)
print_list2(10)


def summa(n):  # рекурсия
    if n == 0:
        return 0
    else:
        return n + summa(n - 1)
print(summa(5))  # 5+4+3+2+1+0 -> 15
