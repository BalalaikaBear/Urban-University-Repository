def mysum(*args):
    if args:  # если ничего не подано - программа не выполняется
        total = args[0]
        for i in args[1:]:
            total += i
        return total


print(mysum("abc", "def"),
      mysum([1,2,3], [4,5,6]),
      mysum(1,2,3),
      mysum("a"),
      mysum((1, 2)),
      mysum(), sep=" -/- ")


def mysum_bigger_than(*args):
    total = 0
    for i in args[1:]:
        if i > args[0]:
            total += i
    return total


print(mysum_bigger_than(10, 5, 20, 30, 6))


def sum_numeric(*args):
    total = 0
    for i in args:
        try:
            total += int(i)
        except:
            pass
    return total


print(sum_numeric(10, 20, "a", "30", "bcd"))


def sum_dict(*kwargs):
    final_dict= {}
    for dictionary in kwargs:
        for key, value in dictionary.items():
            if dict_value := final_dict.get(key):  # если в словаре уже имеется такой ключ, то...
                if isinstance(final_dict[key], list):  # если значение является списком...
                    final_dict[key] = dict_value.append[value]  # добавить объект в список
                else:
                    final_dict[key] = [dict_value, value]  # создать список и добавить туда новый объект
            else:
                final_dict[key] = value  # если такого ключа еще нет -> создать

    return final_dict


print(sum_dict({"a": 1, "hallo": "pi"}, {"a": 2, "potato": 15.0}, {"A": None}))
