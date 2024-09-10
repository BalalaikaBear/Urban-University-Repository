import threading
import time

import requests  # позволяет обращаться к url сайта
from threading import Thread  # мультипоточность


'''
URL = 'https://binaryjazz.us/wp-json/genrenator/v1/genre'  # адрес сайта
res = []  # список данных с сайта

def func(url):
    response = requests.get(URL)  # получение данных с сайта
    page_response = response.json()  # преобразование данных в str
    res.append(page_response)


thr_first = Thread(target=func, args=(URL,))  # Создание потока,
                                           # <target> - функция, которая будет выполняться
                                           # <args> - аргументы, которые будут переданы

#thr_first.start()  # запуск потока
#thr_first.join()  # останавливает выполнение программы, пока не выполнится поток
#print(res)
'''


'''
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
'''

'''
# Обработка ошибок в потоках
def some_func():
    time.sleep(1)
    raise Exception

def thread_func():
    try:
        some_func()
    except Exception:
        print('Exception')

t1 = Thread(target=thread_func)
t2 = Thread(target=thread_func)

t1.start()
t2.start()

t1.join()
t2.join()

# Обработка ошибок в потоках, вариант 2 через excepthook
def except_hook(args):  # при вызове ошибки будет выполняться данная функция
    print(args.thread.name)

threading.excepthook = except_hook  # замена функции при срабатывании ошибки на свою

t1 = Thread(target=some_func)
t2 = Thread(target=some_func)  # -> Thread-5 (some_func)

t1.start()
t2.start()

t1.join()
t2.join()
'''


# ОЧЕРЕДИ В ПОТОКАХ
import queue

def producer(queue):  # функция, создающее сообщение, и затем кладет ее в очередь
    message = 'ping'
    while True:
        queue.put(message)  # кладем сообщение в очередь
        time.sleep(1)

def worker(queue):  # функция, читающая сообщение из очереди
    while True:
        message = queue.get()
        print(message)

q = queue.Queue()

t1 = Thread(target=producer, args=(q, ))
t2 = Thread(target=worker, args=(q, ))

t1.start()
t2.start()

t1.join()
t2.join()
