def find_pair_of_numbers(n,  # для какого числа искать пары
                         limit = 21,  # предел поиска пары
                         is_following_task = True):  # отображение строки или списка (соответствие заданию?)

    result = []

    # генерация чисел (пар)
    for first in range(1, limit):
        for second in range(1, limit):

            if (n % (first + second) == 0  # число кратно сумме пар
                    and first != second):  # числа разные?

                # проверка на одинаковые пары чисел
                if [second, first] not in result:
                    result.append([first, second])  # добавить пары в список

    # вывести строку или список?
    if is_following_task:
        # преобразовать лист в строку
        for char in ["[", "]", " ", ","]:
            result = str(result).replace(char, "")
        return result
    else:
        return result

max_value = 20  # конечный диапазон чисел

# проверка всех значений от 3 до max_value
for i in range(3,max_value+1):
    print(i, "-", find_pair_of_numbers(i, max_value+1, 1))