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
    print(input[0])
    if not (type(data_structure[0]) == float
        or type(data_structure[0]) == int):  # если 1-й элемент не число
        input = [0] + list(input)  # вставить число в начало списка
                                   # 1-е число - сумма
    sum = input[0]
    if len(input) == 1:
        return sum
    else:
        for thing in input[1:]:
            if type(thing) == list or type(thing) == tuple or type(thing) == set:  # если последовательность
                return summator()

data_structure = [
    [1, 2, 3],
    {'a': 4, 'b': 5},
    (6, {'cube': 7, 'drum': 8}),
    "Hello",
    ((), [{(2, 'Urban', ('Urban2', 35))}])
]

print(summator(data_structure))