# from math import inf

def divide(first, second):
    if second == 0 and first >= 0:
        return float("+inf")  # или return inf при подключенной библиотеки
    elif second == 0 and first < 0:
        return float("-inf")
    else:
        return first / second