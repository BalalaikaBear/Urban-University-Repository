def ubbi_dubbi(line):  # мой вариант
    line = line.lower()
    vowels = "aeiouy"  # гласные буквы
    line_list = []

    # разбиение слова на слога
    j = 0  # j - начало слога, i - конец слога
    for i, letter in enumerate(line):
        if letter in vowels:
            line_list.append(line[j:i])
            j = i

    if j != 0:  # добавление окончания
        line_list.append(line[j:])

    return "ub".join(line_list)  # соединение списка из слогов в слово


print(ubbi_dubbi("elephant"))


def ubbi_dubbi(word):  # вариант из книги - последовательное добавление символов
    output = []
    for letter in word:
        if letter in "aeiouy":
            output.append(f"ub{letter}")
        else:
            output.append(letter)

    return "".join(output)


print(ubbi_dubbi("ipython"))
