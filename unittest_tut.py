import unittest

def add(a, b):
    return a + b

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

    def test_sub(self) -> None:  # тест №2
        self.assertEqual(sub(4, -4), 8)

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

