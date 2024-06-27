numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

primes = []
not_primes = []

for i in numbers:
    dividers = set()  # обнуление целых делителей числа
    for j in numbers:
        if i % j == 0:
            dividers.add(j)  # занести в список делитель i-го числа
    if len(dividers) == 2:
        primes.append(i)
    elif len(dividers) > 1:  # исключение 1 как не простого числа
        not_primes.append(i)

print(primes)
print(not_primes)

# для себя - вывод делителей непростых чисел
primes = []
not_primes = {}

for i in numbers:
    dividers = list()  # обнуление целых делителей числа
    for j in numbers:
        if i % j == 0:
            dividers.append(j)  # занести в список делитель i-го числа
    if len(dividers) == 2:
        primes.append(i)
    elif len(dividers) > 1:  # исключение 1 как не простого числа
        not_primes.update({i: dividers})

print(primes)
print(not_primes)
