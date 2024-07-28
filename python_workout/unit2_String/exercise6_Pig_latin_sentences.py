from exercise5_Pig_latin import *


def pl_sentence(letter):
    new_sentence = []

    for word in letter.split():
        new_sentence.append(pig_latin(word))

    return " ".join(new_sentence).capitalize()


print(pl_sentence("this is a test translation!"))


def change_words(_list):
    # создание пустого списка типа [None, None, None], [None, None...
    new_list = [ [None for x in range (len(_list)) ] ]
    for i in range(len(_list) - 1):
        new_list.append( [None for x in range (len(_list)) ] )
    #print(new_list)

    # перестановка значений
    for i, sentence in enumerate(_list):
        for j, word in enumerate(sentence.split()):
            new_list[j][i] = word

    # объединение списков внутри списка
    for i, sentence in enumerate(new_list):
        new_list[i] = " ".join(sentence)

    return new_list


print(change_words(["abc def ghi", "jkl mno pqr", "stu vwx yz"]))
