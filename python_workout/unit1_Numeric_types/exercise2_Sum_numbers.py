def mysum(*numbers, _sum=0):
    if _sum:
        numbers = list(numbers)
        numbers.append(_sum)

    for number in numbers:
        _sum += number

    return {"sum": _sum, "average": _sum / len(numbers), "len": len(numbers)}


print(mysum(1, 2, 4, 5, 6, 8, _sum=10))


def words_len(*words):
    """
    Принимает слова. Возвращает кортеж из чисел:
    - длины самого короткого слова
    - длины самого длинного слова
    - средняя длина слова
    """
    short_word = words[0]
    long_word = words[0]
    total_length = 0

    for word in words:
        total_length += len(word)
        if len(short_word) > len(word):
            short_word = word
        if len(long_word) < len(word):
            long_word = word

    return len(short_word), len(long_word), total_length / len(words)


print(words_len("Mark", "Hi", "Balenciaga"))


def sum_all(*entities, _sum=0):
    """
    Принимает объекты. Суммирует только объекты, которые являются числами, или могут быть преобразованы в числа.
    """
    for entity in entities:
        if isinstance(entity, (int, float)):
            _sum += entity
        elif isinstance(entity, str):
            _sum += len(entity)
        else:
            continue

    return _sum


print(sum_all(1, 4, "Fives", ["list"], _sum=10))
