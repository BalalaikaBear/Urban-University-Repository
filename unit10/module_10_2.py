from threading import Thread  # мультипоточность
import time

class Knight(Thread):
    def __init__(self, name: str, power: int):
        self.name = name
        self.power = power
        super().__init__()

    def run(self):
        print(f'{self.name}, на нас напали!')

        days = 1
        enemies = 100
        while enemies:
            enemies -= self.power
            print(f'{self.name} сражается {days} день(дня)..., осталось {enemies}')
            days += 1
            time.sleep(1)

        print(f'{self.name} одержал победу спустя {days - 1} дней(дня)!')


knights = (Knight('Sir Lancelot', 10),
           Knight("Sir Galahad", 20))

for knight in knights:
    knight.start()

for knight in knights:
    knight.join()
