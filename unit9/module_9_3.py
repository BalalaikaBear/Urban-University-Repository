first = ['Strings', 'Student', 'Computers']
second = ['Строка', 'Урбан', 'Компьютер']

first_result = (len(x) - len(y) for x, y in zip(first, second) if len(x) != len(y))
second_result = (len(x) == len(y) for i, x in enumerate(first) for j, y in enumerate(second) if i == j)

print(list(first_result))
print(list(second_result))
