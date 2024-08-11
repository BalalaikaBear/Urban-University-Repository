from operator import itemgetter

PEOPLE = [{"first": "Vlad", "last": "Ivan", "number": 5550451},
          {"first": "Katya", "last": "Smirnova", "number": 5551234},
          {"first": "Nikolas", "last": "Petrov", "number": 5556969}]


def alphabetize_names(contacts):
    # через отдельную функцию
    for i in sorted(contacts, key=person_dict_to_list):
        print(f"{i["last"]}, {i["first"]}, {i["number"]}")

def person_dict_to_list(dictionary):
    return [dictionary["last"], dictionary["first"]]


alphabetize_names(PEOPLE)


def alphabetize_names(contacts):
    # lambda возвращает анонимную функцию
    for i in sorted(contacts, key=lambda x: [x["last"], x["first"]]):
        print(f"{i["last"]}, {i["first"]}, {i["number"]}")


alphabetize_names(PEOPLE)


def alphabetize_names(contacts):
    # через оператор itemgetter (itemgetter возвращает функцию!)
    for i in sorted(contacts, key=itemgetter("last", "first")):  # itemgetter возвращает кортеж (<значение last>,
        print(f"{i["last"]}, {i["first"]}, {i["number"]}")       #                               <значение first>)


alphabetize_names(PEOPLE)


def vowels(word):
    vowels = 0
    for letter in word:
        if letter in "aeyuio":
            vowels += 1
    return vowels, word


print(sorted([1, 2, -3, -11], key=abs))  # сортировка по модулю числа
print(sorted(["banana", "soup", "apple", "milk"], key=vowels))  # сортировка по количеству слагаемых и затем по алфавиту
print(sorted([[10], [1, 2, 3], []], key=sum))  # сортировка по сумме значений в списке
