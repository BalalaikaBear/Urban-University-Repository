import random

def is_prime(func):
    def wrapper(*args, **kwargs):
        func_result = func(*args, **kwargs)

        n = 0
        for i in range(2, func_result // 2+1):
            if func_result % i == 0:
                n += 1
        if n == 0:
            print("Простое")
        else:
            print("Составное")

        return func_result
    return wrapper

@is_prime
def sum_three(*numbers):
    return sum(numbers)


result = sum_three(random.randint(1, 100),
                   random.randint(1, 100),
                   random.randint(1, 100))
print(result)
