import random

def find_pairs_of_number(n,  # для какого числа искать пары
                         is_following_task = True):  # отображение строки или списка (соответствие заданию?)

    result = []

    # генерация чисел (пар)
    for first in range(1, n):
        for second in range(1, n):

            if (n % (first + second) == 0  # число кратно сумме пар?
                    and first != second  # числа разные?
                    and [second, first] not in result):  # проверка на одинаковые пары
                result.append([first, second])  # добавить пары в список

    # вывести строку или список?
    if is_following_task:
        # преобразовать список в строку
        for char in ["[", "]", " ", ","]:
            result = str(result).replace(char, "")
        return result
    else:
        return result


min_value = 3  # начальный диапазон чисел
max_value = 20  # конечный диапазон чисел

# вывод рандомного числа и его пар
random_value = random.randint(min_value, max_value)
print(random_value, "-", find_pairs_of_number(random_value))

# проверка всех значений от min_value до max_value
# for i in range(3,max_value+1):
#     print(i, "-", find_pair_of_numbers(i, 1))