# перемножение всех цифр числа, игнорируя 0, через метод рекурсии
def get_multiplied_digits(number):
    str_number = str(number)  # преобразоваие числа в строку
    first = int(str_number[0])  # первая цифра строки
    if len(str_number) > 1:
        return first * get_multiplied_digits(int(str_number[1:]))  # при преобразовании строки в числа первые нули убираются
    else:
        return first


print(get_multiplied_digits(40203))