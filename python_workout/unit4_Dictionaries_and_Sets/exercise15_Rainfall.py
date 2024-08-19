from collections import Counter

def get_rainfall():
    dic = Counter()

    while city := input("Введите название города: ").strip():
        rain = int(input("Введите количество осадков: "))
        list_in_dic = dic.get(city, [])
        list_in_dic.append(rain)
        dic[city] = list_in_dic

    for city, rains in dic.items():
        i, summ = 0, 0
        for value in rains:
            summ += value
            i += 1
        print(f"Город {city}: общее кол-во осадков: {summ}, среднее значение осадков: {summ/i}")

get_rainfall()

def words_len(url):
    words = Counter()

    with open(url, "r", encoding="utf-8") as file:  # чтение файла
        text = file.read()

    for word in text.split():  # количество встречаемых слов определенной длины
        words[len(word)] += 1

    print(words)

words_len("The Strange Case Of Dr. Jekyll And Mr. Hyde.txt")
