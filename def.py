import random

def say_hello(user = "Admin"):  # def <название функции> (<локальные данные>)  <user = ""> - значение по умолчанию
    print(f'Hello {user}')

def lottery():  # возвращающая функция
    tickets = [1,2,3,4,5,6,7,8,9]
    win = random.choice(tickets)
    return win  # останавливает выполнение функции
    print("Alarm!")

def lottery2(*args, **kwargs):  # *<название переменной> - несколько значений
    tickets = [1,2,3,4,5,6,7,8,9]
    win = random.choice(tickets)
    print(*args)
    return win

def test(a = 2, b = True):
    print(a, b)

def printer():
    global a, b  # возможность перезаписывания глобальных имен
    a = True
    b = False
    print(a, b)
a = 10
b = 15
print(a, b)
printer()


say_hello()
say_hello("Arnold")
say_hello("Mark")

print(lottery())

print(lottery2(1,2,3,4,5,6,))

test(*[1, 2])  # * - распаковка списка