import unittest
import unittest_tut  # файл с тестами

calcST: unittest.TestSuite = unittest.TestSuite()
#calcST.addTest(unittest.makeSuite(unittest_tut.CalcTest))  # добавление тестов в TestSuite (не работает в версии Python > 3.13
calcST.addTest(unittest.TestLoader().loadTestsFromTestCase(unittest_tut.CalcTest))  # добавление модуля с тестами в TestSuite

runner: unittest.runner.TextTestRunner = unittest.TextTestRunner(verbosity=2)
# <verbosity=1> - стандартное отображение (по умолчанию)
# <verbosity=2> - отображает список пройденных тестов
runner.run(calcST)  # запуск тестов отдельного файла
