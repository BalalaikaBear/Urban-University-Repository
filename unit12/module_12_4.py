import logging
import unittest

class Runner:
    def __init__(self, name, speed=5):
        if isinstance(name, str):
            self.name = name
        else:
            raise TypeError(f'Имя может быть только строкой, передано {type(name).__name__}')
        self.distance = 0
        if speed > 0:
            self.speed = speed
        else:
            raise ValueError(f'Скорость не может быть отрицательной, сейчас {speed}')

    def run(self):
        self.distance += self.speed * 2

    def walk(self):
        self.distance += self.speed

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, Runner):
            return self.name == other.name


class Tournament:
    def __init__(self, distance, *participants):
        self.full_distance = distance
        self.participants = list(participants)

    def start(self):
        finishers = {}
        place = 1
        while self.participants:
            for participant in self.participants:
                participant.run()
                if participant.distance >= self.full_distance:
                    finishers[place] = participant
                    place += 1
                    self.participants.remove(participant)

        return finishers

class RunnerTest(unittest.TestCase):

    def test_wall(self) -> None:
        try:
            obj: Runner = Runner('name', speed=-2)
            for _ in range(10):
                obj.walk()
            self.assertEqual(obj.distance, 50)
            logging.info('"test_walk" выполнен успешно')
        except:
            logging.warning('Неверная скорость для Runner')

    def test_run(self) -> None:
        try:
            obj: Runner = Runner(False)
            for _ in range(10):
                obj.run()
            self.assertEqual(obj.distance, 100)
            logging.info('"test_run" выполнен успешно')
        except TypeError:
            logging.warning("Неверный тип данных для объекта Runner")

    def test_challenge(self) -> None:
        obj_a: Runner = Runner('Alfred')
        obj_b: Runner = Runner('Billy')
        for _ in range(10):
            obj_a.walk()
            obj_b.run()
        self.assertNotEqual(obj_a.distance, obj_b.distance)

logging.basicConfig(level=logging.INFO,  # с какого уровня воспринимается сообщение (INFO = 20)
                    filemode='w',  # запись файла
                    filename='runner_tests.log',  # имя файла
                    encoding='utf-8',  # кодировка
                    format='LOGGING LEVEL: %(levelno)s\n - %(message)s\n')  # оформление сообщения в логе
