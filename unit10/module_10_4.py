from threading import Thread
from time import sleep
from random import randint
from queue import Queue
from colorama import Fore

def h(word, color = 'g'):  # highlight - выделить текст
    if color == 'g':
        return Fore.GREEN + str(word) + Fore.RESET
    elif color == 'p':
        return Fore.MAGENTA + str(word) + Fore.RESET

class Guest(Thread):
    """Гость"""
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def run(self):
        sleep(randint(3, 10))

class Table:
    """Столик в кафе"""
    def __init__(self, number: int, guest: Guest = None):
        self.number = number
        self.guest = guest

    def is_free(self):
        """Занят ли столик?"""
        if self.guest is None:
            return True
        else:
            return False

class Cafe:
    """Кафе"""
    def __init__(self, *tables: tuple[Table]):
        self.tables = tables
        self.queue = Queue()

    def guest_arrival(self, *guests: tuple[Guest]):
        """Принимает гостя в кафе. Если свободного стола нет - отправляет гостя в очередь"""
        for guest in guests:
            # поиск пустого столика
            for table in self.tables:
                if table.is_free():
                    tables_are_free = True
                    print(f'{h(guest.name, 'p')} сел(а) за стол номер {h(table.number)}')
                    table.guest = guest
                    guest.start()  # посетитель начал есть (запуск потока)
                    break  # остановка поиска пустых столиков
                else:
                    tables_are_free = False

            # отправить посетителя в очередь, если столы заняты
            if tables_are_free is False:
                self.queue.put(guest)
                print(f'{h(guest.name, 'p')} в очереди')

    def discuss_guests(self):
        """Обслуживание посетителей в кафе"""
        eating_guests = len(guests)  # количество посетителей, которых надо обслужить
        while eating_guests or not self.queue.empty():

            for table in self.tables:
                # поел ли посетитель?
                if not table.is_free() and not table.guest.is_alive():  # добавлена проверка на занятость стола, иначе ошибка (2-е условие не проверяется)
                    print(f'{h(table.guest.name, 'p')} покушал(-а) и ушёл(ушла)')
                    print(f'Стол номер {h(table.number)} {h('свободен')}, осталось гостей: {h(eating_guests - 1)}')
                    table.guest = None  # освобождение столика
                    eating_guests -= 1  # посетитель обслужен

                # если освободился столик при живой очереди -> посетитель занимает столик
                if not self.queue.empty() and table.is_free():
                    guest = self.queue.get()
                    table.guest = guest  # занятие столика посетителем
                    print(f'{h(guest.name, 'p')} вышел(-ла) из очереди и сел(-а) за стол номер {h(table.number)}')
                    guest.start()  # посетитель начал есть (запуск потока)
                    break  # остановка поиска следующих пустых столиков


# создание столов в кафе
tables = [Table(number) for number in range(1, 6)]

# имена гостей
guests_names = ['Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
                'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra']

# Создание гостей
guests = [Guest(name) for name in guests_names]

# Заполнение кафе столами
cafe = Cafe(*tables)

# Приём гостей
cafe.guest_arrival(*guests)

# Обслуживание гостей
cafe.discuss_guests()

