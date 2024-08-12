# ASCII и UNICODE (кодировка)
A = []
for i in "Hello human": A.append(ord(i))  # преобразование слова в кодированное число
print("1:", A)
print("2:", [chr(i) for i in range(128)])  # символы из таблицы UNICODE
print("3:", hex(ord("h")))  # преобразование символа в шестнадцатеричный формат
print("4:", type(bb := b"\x68"))  # bytes - байт
print("5:", bb.decode())  # из шестнадцатеричного формата в символьный


# Файлы в операционной системе
import os

print("10: 'Текущая директория' -", os.getcwd())  # возвращает путь до данного файла
if not os.path.exists("test_folder"):  # проверка на существование директории
    os.mkdir("test_folder")  # создание папки, при повторном срабатывании вызывает ошибку FileExistsError
    os.chdir("test_folder")
else:
    os.chdir("test_folder")  # изменение директории
print("11: 'Текущая директория' -", os.getcwd())
if not os.path.exists(r"second_test_folder\the_third"):  # r перед строкой игнорирует разделители строки
    os.makedirs(r"second_test_folder\the_third")  # создание папок, при повторном срабатывании вызывает ошибку FileExistsError
print("12:", os.listdir())  # посмотреть список файлов, находящихся в рабочем пространстве
for i in os.walk("."):  # Просмотр вложенности файлов, "." - обозначает текущую директорию
    print("12.a:", i)

os.chdir(r"C:\Users\eight\pythonProjects\Urban-University-Repository\python_workout")
print("13: 'Текущая директория' -", os.getcwd())
for i in os.walk("."):
    print("13.a:", i)  # выводит кортеж из (<положение дирректории>, [<список папок>], [<список файлов>])

os.chdir(r"C:\Users\eight\pythonProjects\Urban-University-Repository\unit6")
print("15:", os.listdir())  # выводит все файлы и папки в директории
file = [f for f in os.listdir() if os.path.isfile(f)]  # отображает только файлы в директории
dirs = [d for d in os.listdir() if os.path.isdir(d)]  # отображает только папки в директории
print("16:", "files:", file, "directories:", dirs)
#os.startfile(file[3])  # запустить указанный файл
print("17:", os.stat(file[3]))  # выводит информацию об файле
print("17.a:", os.stat(file[3]).st_size)  # выведет только информацию о размере файла в БАЙТАХ
#os.system("pip install random")  # работа с командной строкой
