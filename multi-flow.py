import requests  # позволяет обращаться к url сайта
from threading import Thread  # мультипоточность

URL = 'https://binaryjazz.us/wp-json/genrenator/v1/genre'  # адрес сайта
res = []  # список данных с сайта

def func(url):
    response = requests.get(URL)  # получение данных с сайта
    page_response = response.json()  # преобразование данных в str
    res.append(page_response)


thr_first = Thread(target=func, args=(URL,))  # Создание потока,
                                           # <target> - функция, которая будет выполняться
                                           # <args> - аргументы, которые будут переданы

thr_first.start()  # запуск потока
thr_first.join()  # останавливает выполнение программы, пока не выполнится поток
print(res)


# Мультипоточность через собственный класс
class Getter(Thread):
    results = []
    URL = 'https://binaryjazz.us/wp-json/genrenator/v1/genre'

    def run(self):
        response = requests.get(self.URL)
        Getter.results.append(response.json())

threads = []

for i in range(5):
    thread = Getter()
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print(Getter.results)