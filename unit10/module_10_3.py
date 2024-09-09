from threading import Thread, Lock
import random
import time

class Bank:
    def __init__(self, balance: int = 0, lock: Lock = Lock()):
        self.balance = balance
        self.lock = lock

    def deposit(self):
        for _ in range(100):
            random_number = random.randint(50, 500)
            self.balance += random_number
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()
            print(f'Пополнение: {random_number}. Баланс: {self.balance}')
            time.sleep(0.001)

    def take(self):
        for _ in range(100):
            random_number = random.randint(50, 500)
            print(f'Запрос на {random_number}')
            if random_number <= self.balance:
                self.balance -= random_number
                print(f'Снятие: {random_number}. Баланс: {self.balance}')
            else:
                print('Запрос отклонён, недостаточно средств')
                self.lock.acquire()
            #time.sleep(0.001)

bk = Bank()

th_1 = Thread(target=Bank.deposit, args=(bk,))
th_2 = Thread(target=Bank.take, args=(bk,))

th_1.start()
th_2.start()

th_1.join()
th_1.join()

print(f'Итоговый баланс: {bk.balance}')