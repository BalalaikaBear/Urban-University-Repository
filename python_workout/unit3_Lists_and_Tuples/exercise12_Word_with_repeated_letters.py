from collections import Counter

test = ["this", "is", "an", "elementary", "test", "example", "bbbb"]


def most_repeating_word(words):
    """
    Возвращает слово с самыми повторяемыми буквами
    """
    return max(words, key=lambda word: Counter(word).most_common(1)[0][1])
    # return max(words, key=most_repeating_letter_count)


def most_repeating_letter_count(word):
    return Counter(word).most_common(1)[0][1]


print(most_repeating_word(test))


def most_repeating_word_with_vowels(words):
    return max(words, key=most_repeating_vowels)


def most_repeating_vowels(word):
    for letter in Counter(word).most_common():  # буквы отсортированы по частоте встречаемости
        if letter[0] in "aeyuio":  # если гласная
            return letter[1]  # вернуть количество встречаемости этой гласной
    return 0  # иначе вернуть ноль


print(most_repeating_word_with_vowels(test))
