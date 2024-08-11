def first_last(a):
    return a[::len(a)-1]


print(first_last([0, 10, 100, "a"]), first_last("abc"))


def new_max(a):
    max_item = a[0]
    for i in a[1:]:
        if i > max_item:
            max_item = i
    return max_item


print(new_max([0, 10, 100]), new_max("adDc"), new_max(("10", "ten", "eleven", "tens")))


def even_odd_sums(a):
    """
    Возвращает сумму нечетных и четных индексов
    """
    return [sum(a[::2]), sum(a[1::2])]


print(even_odd_sums([10, 20, 30, 40, 50, 60]))


def plus_minus(a):
    """
    10 + 20 - 30 + 40 - 50 + ...
    """
    return a[0] + sum(a[1::2]) - sum(a[2::2])


print(plus_minus([10, 20, 30, 40, 50, 60]))
