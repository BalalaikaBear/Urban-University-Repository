first = int(input("Введите первое число:"))
second = int(input("Введите второе число:"))
third = int(input("Введите третье число:"))

# вариант 1 - в лоб
if first == second and first == third:
    print("Одинаковых чисел:", 3)
elif first == second or first == third or second == third:
    print("Одинаковых чисел:", 2)
else:
    print("Одинаковых чисел:", 0)

# вариант 2 - через множество
t = {first, second, third}
if len(t) == 1:
    print("Одинаковых чисел:", 3)
elif len(t) == 2:
    print("Одинаковых чисел:", 2)
else:
    print("Одинаковых чисел:", 0)

# вариант 3 - через множество + оптимизированный if (поскольку вариант 0 самый вероятный)
t = {first, second, third}
if len(t) == 3: print("Одинаковых чисел:", 0)
else: print("Одинаковых чисел:", 4-len(t))