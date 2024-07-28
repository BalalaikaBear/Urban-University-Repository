def hex_output():
    decnum = 0
    hex_number = input("Введите шестнадцатеричное число для преобразования: ")
    for power, digit in enumerate(reversed(hex_number)):
        decnum += int(digit, 16) * (16 ** power)
    print(decnum)

    # print(int(hex_number, 16))  # постой способ


#hex_output()


def strange_name():
    name = input("Введите ваше имя: ")
    for index in range(len(name) + 1):
        print(name[:index], end="")


strange_name()
