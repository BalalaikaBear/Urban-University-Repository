import random


def guessing_game():
    random_value = random.randint(0, 100)  # генерация числа
    count_fails = 3  # количество попыток

    while count_fails:
        try:
            input_value = int(input("Введите целое число: "))

            if input_value == random_value:
                print("Вы угадали")
                break
            elif input_value > random_value:
                count_fails -= 1
                if count_fails:
                    print("Слишком большое, осталось попыток:", count_fails)
                else:
                    print("Слишком большое, попытки закончились. Было загадано число", random_value)
            else:
                count_fails -= 1
                if count_fails:
                    print("Слишком маленькое, осталось попыток:", count_fails)
                else:
                    print("Слишком маленькое, попытки закончились. Было загадано число", random_value)

        except ValueError:  # если введено не число
            print(f"Вы ввели не целое число!")


guessing_game()
