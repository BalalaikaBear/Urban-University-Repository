def custom_write(file_name, strings):
    file = open(file_name, "w", encoding="utf-8")  # открытие файла для записи

    # запись текста в файл с параллельным сохранением информации в словарь
    strings_positions = {}  # { (<номер строки>, <номер байта>): <текст в строке> }
    for i, string in enumerate(strings):
        strings_positions[(i+1, file.tell())] = string
        file.write(f"{string}\n")

    file.close()
    return strings_positions


info = [
    'Text for tell.',
    'Используйте кодировку utf-8.',
    'Because there are 2 languages!',
    'Спасибо!'
    ]

result = custom_write("module_7_2.txt", info)
for elem in result.items():
    print(elem)