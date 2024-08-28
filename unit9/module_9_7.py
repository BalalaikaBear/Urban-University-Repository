import math, random

def is_prime(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        if result == 2:
            print("Простое")
        for i in range(2, int(math.sqrt(result))+1):
            if result % i == 0:
                print("Составное")
                break
            else:
                print("Простое")
                break
        return result
    return wrapper

@is_prime
def sum_three(*numbers):
    return sum(numbers)


result = sum_three(random.randint(1, 100),
                   random.randint(1, 100),
                   random.randint(1, 100))
print(result)
