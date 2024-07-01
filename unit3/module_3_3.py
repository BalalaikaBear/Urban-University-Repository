def print_params(a = 1, b = "строка", c = True):
    print(a, b, c)

print_params()
print_params(b = 25)
print_params(c = [1, 2, 3])

values_list = [42, {10, "Hi"}, "Mark"]
values_dict = {"a": False, "b": None, "c": 121}

print_params(*values_list)
print_params(**values_dict)

values_list_2 = [bool(1), 70]
print_params(*values_list_2)
