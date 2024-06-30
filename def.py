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
test(*[1, 2])  # * - распаковка списка

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






