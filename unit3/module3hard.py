def summator(*n):
    _sum = 0

    # отладка
#    print("Summator:", sum, type(n), n)

    if len(n) == 1:  # если последовательность размером в 1 элемент
        n = n[0]  # раскрыть последовательность

    if isinstance(n, (int, float)):  # если первый элемент число, занести число в sum
        _sum = n

    # отладка
#    print("Summator:", sum, type(n), n)

    if isinstance(n, (int, float)):  # если число
        return _sum
    elif isinstance(n, str):  # если строка
        return _sum + len(n)
    elif isinstance(n, (list, tuple, set)):  # если последовательность
        n = list(n)  # преобразование set в list (без этой строки ошибка, поскольку set is not subscriptable)
        if len(n) == 0:
            return _sum
        else:
            return _sum + summator(n[0]) + summator(n[1:])
    elif isinstance(n, dict):  # если словарь
        return _sum + summator(list(n.items()))


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
