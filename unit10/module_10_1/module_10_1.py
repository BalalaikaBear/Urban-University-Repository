from threading import Thread
from datetime import datetime
import time

def write_words(word_count, file_name):
    with open(file_name, "w", encoding="utf-8") as file:
        for number in range(1, word_count+1):
            file.write(f"Какое-то слово №{number}\n")
            time.sleep(0.1)
    print(f"Завершилась запись в файл {file_name}")

# Поочередная работа функций
time_start = datetime.now()

for index, count in enumerate([10, 30, 200, 100]):
    write_words(count, f"example{index+1}.txt")

print(f"Поочередная работа функций: {datetime.now() - time_start}")

# Работа потоков
threads = []
for index, count in enumerate([10, 30, 200, 100]):
    threads.append(Thread(target=write_words, args=(count, f"example{index+5}.txt")))

time_start = datetime.now()

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print(f"Работа потоков: {datetime.now() - time_start}")
