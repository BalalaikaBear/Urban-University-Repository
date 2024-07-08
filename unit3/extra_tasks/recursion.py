# exercise 1
def factorial(n):
    if n == 1:
        return 1
    else:
        return n*factorial(n-1)

print("  1:", factorial(5))


# exercise 2
def list_sum(n):
    length = len(n)
    list_ = []
    for index in range(length):
        list_.append(n[index])
    if length == 0:
        return 0
    else:
        return list_[0] + list_sum(list_[1:])

print("2.1:", list_sum([1, 2, 3]))


#exercise 2 / вариант 2
def list_sum2(n):
    if len(n) == 0:
        return 0
    else:
        return n[0] + list_sum2(n[1:])

print("2.2:", list_sum2([0, -5, 5, 10.3]))


# exercise 3
def power(a, n):
    a_ = a  # неясно зачем создавать новую переменную
    n_ = n
    if n_ == 1:
        return a_
    else:
        return a_*power(a_, n_-1)

print("  3:", power(5, 2))


# exercise 4
def rabits_progress(months, rabits=2, switch=True):
    print("Зайцев:",rabits, ", Месяцев осталось:", months)
    if months <= 1:
        return rabits // 2
    else:
        if switch:  # -2 месяца
            return rabits_progress(months-2, rabits=rabits*2, switch=False)
        else:  # -1 месяц
            return rabits_progress(months-1, rabits=rabits*2, switch=True)

print("  4: Пар зайцев:", rabits_progress(12))