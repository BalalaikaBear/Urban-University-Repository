def collatz(number):
    global index
    if number % 2 == 0:
        print("Итерация:", index, "->", number // 2)
        index += 1
        return number // 2
    else:
        print("Итерация:", index, "->", 3*number + 1)
        index += 1
        return 3*number + 1

def input_function():
    try:  # выполняется при вызове функции
        return int(input("Введите число: "))
    except:  # если возникает ошибка - выполнять данный код
        print("Ошибка! Введите целое число")
        return input_function()

index = 1  # количество итераций (глобальная переменная)

number = input_function()
while number != 1:
    number = collatz(number)
