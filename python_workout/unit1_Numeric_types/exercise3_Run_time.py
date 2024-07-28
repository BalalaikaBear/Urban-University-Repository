def run_timing():
    input_list = []

    while True:
        output = input("Введите время пробега 10 км: ")

        if output:  # если было что-то введено, то...
            try:
                input_list.append(float(output))
            except ValueError:
                print("Введите число!")
        else:
            break

    print(f"Средний показатель {sum(input_list) / len(input_list):.2f}, более {len(input_list)} пробежек")


#run_timing()


def float_numbers(number, before, after):
    # разбиение числа с плавающей точкой на 2 отдельных числа
    numbers_before, numbers_after = str(number).split(".")

    # необходимые числа до и после запятой (точки)
    before = numbers_before[-before:]
    after = numbers_after[:after]

    # создание и вывод требуемого числа
    new_float = float(before + "." + after)
    return new_float


print(float_numbers(123.678, 2, 1))


def decimal_math(a, b):
    import decimal
    A = decimal.Decimal(str(a))
    B = decimal.Decimal(str(b))
    return A + B


print(decimal_math(.1, .2))
