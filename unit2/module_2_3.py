my_list = [42, 69, 322, 13, 0, 99, -5, 9, 8, 7, -6, 5]

# вариант 1
i = 0
while i < len(my_list):
    if my_list[i] < 0:
        break
    elif my_list[i] > 0:
        print(my_list[i])
    i += 1

print("")  # отступ

# вариант 2 - с применением continue
i = 0
while i < len(my_list):
    i += 1
    if my_list[i-1] == 0:
        continue
    elif my_list[i-1] < 0:
        break
    print(my_list[i-1])
