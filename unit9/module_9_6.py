def all_variants(text):
    for flag in range(len(text)):
        for char in text[flag:]:  # проход по всем символам после flag
            yield text[:flag] + char

a = all_variants("abc")
for i in a:
    print(i)
