def pig_latin(line):
    line = line.lower()
    vowels = "aeiouy"  # гласные буквы
    dif_vowels_amount = 0  # счетчик разных гласных в слове

    # учет заканчивающей пунктуации
    end_letter = ""
    if line[-1] in ".,!?:;":
        end_letter = line[-1]
        line = line[:-1]

    # переписывание слова
    if line[0] in vowels:
        return line + "way" + end_letter
    else:
        # подсчет разных гласных в слове
        for letter in line:
            if letter in vowels:
                dif_vowels_amount += 1
                vowels.replace(letter, "")

        if dif_vowels_amount == 2:
            return line + "way" + end_letter
        return line[1:] + line[0] + "ay" + end_letter


if __name__ == "__main__":
    print(pig_latin("Python!"))
    print(pig_latin("Wine"))
    print(pig_latin("Ice"))
    print(pig_latin("Car"))
