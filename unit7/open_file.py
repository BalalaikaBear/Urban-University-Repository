import random
from pprint import pprint


filename = "The Strange Case Of Dr. Jekyll And Mr. Hyde.txt"

file = open(filename, "r", encoding="utf-8")  # режимы открытия файла:
                            # r - read - чтение
                            # w - write - запись
                            # a - append - добавление
                            # x - create an new file and open it for writing
                            # b - binary mode
                            # t - text mode (default)
                            # + - open a disk file for updating (reading and writing)

print(file)  # -> <_io.TextIOWrapper name='The Strange Case Of Dr. Jekyll And Mr. Hyde.txt' mode='r' encoding='utf-8'>
             #     объект            название файла                                         режим открытия, кодировка (по умолчанию - 'cp1251')

print(file.tell())  # курсор в файле (при открытии файла находится в начале -> 0)
pprint(file.read())  # вывод файла в командную строку
print(file.tell())  # курсор находится в конце файла -> 141365
pprint(file.read())  # при повторном вызове вернет пустую строку
file.seek(141360)  # поставить курсор в указанное место
pprint(file.read())
file.close()  # закрытие файла

# запись в файле
file = open("sample.txt", "w")
file.write(str(random.randint(0, 255)))
pprint(file.read())  # -> выдаст ошибку поскольку он открыт в режиме записи
file.close()