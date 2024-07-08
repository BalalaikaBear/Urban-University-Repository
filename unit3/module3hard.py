#def summator(input):
#    print(input)
#    if not (type(data_structure[0]) == float
#            or type(data_structure[0]) == int):  # если 1-й элемент не число
#        input = [0] + list(input)  # вставить число в начало списка
#                                   # 1-е число - сумма
#    sum = input[0]
#    if len(input) == 1:
#        return sum  # вывод конечного числа
#    else:
#        # вся логика
#        for thing in input[1:]:
#            if isinstance(thing, str):  # если str
#                return [sum + len(thing)]
#            elif type(thing) == float or type(thing) == int:  # если число
#                return [sum + thing]
#            elif type(thing) == list or type(thing) == tuple or type(thing) == set:  # если последовательность
#                return summator([sum] + list(thing))
#            elif isinstance(thing, dict):  # если словарь
#                for i, j in thing.items():
#                    return summator([sum, i, j])

def summator(*input):
    input = list(input)
    print(input)
    if not (type(data_structure[0]) == float
        or type(data_structure[0]) == int):  # если 1-й элемент не число
        input = [0] + list(input)  # вставить число в начало списка
        print("check")                           # 1-е число - сумма
    sum = input[0]
    if len(input) == 1 and (type(input) == int or type(input) == float):  # последнее число? -> завершить
        return sum
    else:
        # основная логика
        for thing in input[1:]:
            if type(thing) == list or type(thing) == tuple or type(thing) == set:  # если последовательность
                print("list")
                return summator(sum, thing)
            elif isinstance(thing, str):  # если str
                print("str")
                return sum + len(thing)
            elif type(thing) == float or type(thing) == int:  # если число
                print("int")
                return sum + thing
            elif isinstance(thing, dict):  # если словарь
                print("dict")
                for i, j in thing.items():
                    return summator(sum, i, j)


def test(*input):
    print(input)

data_structure = [
    [1, 2, 3],
    {'a': 4, 'b': 5},
    (6, {'cube': 7, 'drum': 8}),
    "Hello",
    ((), [{(2, 'Urban', ('Urban2', 35))}])
]

test(0, data_structure)
print(summator(data_structure))