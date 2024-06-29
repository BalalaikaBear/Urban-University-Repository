def count_calls():  # функция подсчитывает вызовы остальных функций
    global calls
    calls += 1

def string_info(string):  # принимает аргумент - строку и возвращает кортеж из: длины этой строки, строку в верхнем регистре, строку в нижнем регистре
    count_calls()

    return tuple([len(string), str(string).upper(), str(string).lower()])

def is_contains(string, list_to_search):  # есть ли в списке данная строка
    count_calls()

    count = 0  # счетчик цикла for
    for i in list_to_search:
        list_to_search[count] = str(i).lower()  # преобразовать все элементы в списке в нижний регистр
        count += 1

    if string.lower() in list_to_search:
        return True
    else:
        return False

calls = 0

print(string_info('Capybara'))
print(string_info('Armageddon'))
print(is_contains('Urban', ['ban', 'BaNaN', 'urBAN'])) # Urban ~ urBAN
print(is_contains('cycle', ['recycling', 'cyclic'])) # No matches
print(calls)