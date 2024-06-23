first = int(input("Введите первое число:"))
second = int(input("Введите второе число:"))
third = int(input("Введите третье число:"))

# вариант 1
if first == second and first == third:
    print(3)
elif first == second or first == third or second == third:
    print(2)
else:
    print(0)

# вариант 2
t = {first, second, third}
if len(t) == 1:
    print(3)
elif len(t) == 2:
    print(2)
else:
    print(0)

# вариант 3
t = {first, second, third}
if len(t) == 3: print(0)
else: print(4-len(t))