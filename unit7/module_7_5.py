import os, time
from colorama import Fore


def h(word):  # highlight - выделить текст
    return Fore.BLUE + word + Fore.RESET


directory = os.getcwd()
for root, dirs, files in os.walk("."):
    for i, file in enumerate(files):
        file_path = os.path.join(directory, file)  # указание пути к файлу
        file_time = os.path.getmtime(file)  # время последнего изменения файла
        formatted_time = time.strftime("%m.%d.%Y - %H:%M", time.localtime(file_time))  # отформатированное время
        file_size = os.path.getsize(file)  # получение размера файла
        parent_dir = os.path.dirname(file_path)  # получение родительской директории файла
        print("Обнаружен файл №" + str(i + 1) + ": " + h(file)
              + "; Путь: " + h(file_path)
              + "; Размер: " + h(str(file_size) + " байт")
              + "; Время изменения: " + h(formatted_time)
              + "; Родительская директория: " + h(parent_dir))
