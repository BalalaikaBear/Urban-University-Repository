from threading import Thread  # мультипоточность
import time

# RACE CONDITION / СОСТОЯНИЕ ГОНКИ (встречается в Pyhon ниже версии 3.10)
# Атомарные операции - операции, происходящие в одно действие без прерывания
# - [].append()
# - [].extend()
# - [].sort()


x = 0

def thread_task():
    global x
    for i in range(10_000_000):
        x = x + 1

def main():
    global x
    x = 0

    t1 = Thread(target=thread_task())
    t2 = Thread(target=thread_task())

    t1.start()
    t2.start()

    t1.join()
    t2.join()

#for i in range(10):
#    main()
#    print(x)


# БЛОКИРОВКА - блокирует часть кода, для его выполнения только одним потоком
from threading import Lock

lock = Lock()

def thread_task():
    global x
    for i in range(10_000_000):
        # реализация 1 - ошибка останавливает программу!
        lock.acquire()  # открытие части кода только для 1-го потока
        x = x + 1
        lock.release()  # закрытие

        # реализация 2 - ошибка не останавливает программу
        with lock:
            x = x + 1

        # реализация 3 - ошибка не останавливает программу
        try:
            lock.acquire()
            x = x + 1
        finally:
            lock.release()


# ВЗАИМНАЯ БЛОКИРОВКА
lock1 = Lock()
lock2 = Lock()

def thread_task1():
    with lock1:
        print('thread 1 locked 1 acquired')
        time.sleep(1)
        with lock2:
            print('thread 1 locked 2 acquired')

def thread_task2():
    with lock2:
        print('thread 2 locked 2 acquired')
        time.sleep(1)
        with lock1:
            print('thread 2 locked 1 acquired')

t1 = Thread(target=thread_task1())
t2 = Thread(target=thread_task2())

t1.start()
t2.start()

t1.join()
t2.join()
