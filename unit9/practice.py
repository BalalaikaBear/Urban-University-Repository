# 1 - написать функцию, которая возвращает функцию повторения двух первых символов n раз
# 2 - создать массив функций и применить все функции поочередно к аргументу
# 3 - применить все функции поочередно к массиву аргументов

animal = 'bear'
animals = ['rabbit', 'bear', 'rhino']

# 1
def gen_repeat(n):
    def repeat(animal):
        return (animal[:2] + '-') * n + animal
    return repeat

test_1 = gen_repeat(2)
print(test_1(animal))

# 2
repetitions = [gen_repeat(n) for n in range(1, 4)]
print([func(animal) for func in repetitions])

# 3
print([func(x) for func in repetitions for x in animals])
print([func(x) for x in animals for func in repetitions])

# 4 - имеется функция, которая возвращает результат введения числа a в степень b
# необходимо ускорить ее, чтобы она не делала повторные вычисления
def memorize_func(function):
    memory = {}  # память значений

    def wrapper(*args):
        if args not in memory:  # если данных результатов еще нет в памяти - выполнять функцию
            memory[args] = function(*args)
        return memory[args]

    return wrapper

@memorize_func
def func(a, b):
    return a ** b

print(func(3, 4))
print(func(3, 4))
print(func(3, 45))