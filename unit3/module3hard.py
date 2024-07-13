def summator(*n):
    sum_ = 0

    # отладка
#    print("Summator:", sum, type(n), n)

    if len(n) == 1:  # если последовательность размером в 1 элемент
        n = n[0]  # раскрыть последовательность

    if type(n) == float or type(n) == int:  # если первый элемент число, занести число в sum
        sum_ = n

    # отладка
#    print("Summator:", sum, type(n), n)

    if isinstance(n, int) and isinstance(n, float):  # если число
        return sum_ + n
    elif isinstance(n, str):  # если строка
        return sum_ + len(n)
    elif isinstance(n, list) or isinstance(n, tuple) or isinstance(n, set):  # если последовательность
        n = list(n)  # преобразование set в list (без этой строки ошибка)
        if len(n) == 0:
            return sum_
        else:
            return sum_ + summator(n[0]) + summator(n[1:])
    elif isinstance(n, dict):  # если словарь
        return sum_ + summator(list(n.items()))
    else:  # без него не работает, не понимаю почему (проверка на NoneType?)
        return sum_


data_structure = [
    [1, 2, 3],
    {'a': 4, 'b': 5},
    (6, {'cube': 7, 'drum': 8}),
    "Hello",
    ((), [{(2, 'Urban', ('Urban2', 35))}])
]

check = 2, "Tarja", {"": 11, "fd": 3}, (), [1, 2, "four", {"": 11, "fd": 3}]

#print(summator(check))
print(summator(data_structure))
