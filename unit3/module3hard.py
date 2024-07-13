def summator(*n):
    sum = 0
    #print("Summator:", sum, type(n), n)

    if len(n) == 1 and (type(n[0]) != float or type(n[0]) != int):  # если последовательность размером в 1 элемент
        n = n[0]  # раскрыть последовательность

    if type(n) == float or type(n) == int:  # если первый элемент число, занести число в sum
        sum = n


    print("Summator:", sum, type(n), n)

    if isinstance(n, int) and isinstance(n, float):  # если число
        return sum + n
    elif isinstance(n, str):  # если строка
        return sum + len(n)
    elif isinstance(n, list) or isinstance(n, tuple) or isinstance(n, set):  # если последовательность
        if len(n) == 0:
            return sum
        else:
            if type(n[0]) != int or type(n[0]) != float:
                return sum + summator(n[1:])  # если n[0] == "NoneType"
            else:
                return sum + summator(n[0]) + summator(n[1:])
    elif isinstance(n, dict):  # если словарь
        for i, j in n.items():
            return sum + summator(i, j)

        #return n[0] + summator(n[1:])

data_structure = [
    [1, 2, 3],
    {'a': 4, 'b': 5},
    (6, {'cube': 7, 'drum': 8}),
    "Hello",
    ((), [{(2, 'Urban', ('Urban2', 35))}])
]

print(summator(data_structure))