import unittest
import random
import logging

def add(a, b):
    try:
        a + b  # в случае невыполнения данной операции лог записан не будет
        logging.info(f'Successful summ {a} + {b}')
        return a + b
    except TypeError as err:
        logging.error(f'Type error: {err}', exc_info=True)  # передать в лог информацию об ошибке

def sub(a, b):
    return a - b

class CalcTest(unittest.TestCase):
    def setUp(self):  # запускается перед запуском каждого теста (перед каждой функцией в классе)
        pass

    @classmethod
    def setUpClass(cls):  # запускается перед запуском тестов и только один раз
        pass

    def tearDown(self):  # запускается после завершения каждого теста
        pass

    @classmethod
    def tearDownClass(cls):  # запускается после завершения отработки всех тестов
        pass

    def test_add(self) -> None:  # тест №1
        self.assertEqual(add(10, 15), 25)
        self.assertEqual(add(1, 1), 2)

    @unittest.skip("Причина пропуска теста")  # при запуске теста данная функция не будет проверяться
    def test_sub(self) -> None:  # тест №2
        self.assertEqual(sub(4, -4), 8)

    @unittest.skipIf(random.randint(0, 1), "Причина пропуска теста")  # пропуск теста при True
    def all_tests(self) -> None:
        pass
        self.assertEqual(a, b)  # a = b
        self.assertNotEqual(a, b)  # a != b
        self.assertAlmostEqual(a, b)  # сравнить два числа с допуском до 7-й запятой

        self.assertIs(a, b)  # a is b
        self.assertIsNot(a, b)  # a is not b
        self.assertIsNone(a)  # a is None
        self.assertIsNotNone(a)  # a is not None

        self.assertIn("a", "abc")  # a in b
        self.assertNotIn("a", "abc")  # a not in b

        self.assertTrue(a)  # a is True
        self.assertFalse(a)  # a is False

        self.assertRaises(a)  # была ли вызвана ошибка?

        self.assertGreater(a, b)  # a > b
        self.assertGreaterEqual(a, b)  # a >= b
        self.assertLess(a, b)  # a < b
        self.assertLessEqual(a, b)  # a <= b

if __name__ == '__main__':
    unittest.main()  # запуск тестов

    # логи
    logging.debug('сообщение')     # 1. сообщения уровня debug
    logging.info('сообщение')      # 2. информационные логи
    logging.warning('сообщение')   # 3. сообщения о предупреждениях
    logging.error('сообщение')     # 4. сообщения об ошибках
    logging.critical('сообщение')  # 5. сообщения о критических ошибках

    logging.basicConfig(level=logging.INFO,   # <level> - с какого уровня воспринимается сообщение
                        filemode='w',         # <filemode> - запись файла
                        filename='logs.log',  # <filename> - имя файла
                        format='%(asctime)s | %(levelname)s | %(message)s')  # <format> - оформление сообщения в логе
