import unittest
import module_12_3

calcST: unittest.TestSuite = unittest.TestSuite()

# добавление тестов из модулей в TestSuite
calcST.addTest(unittest.TestLoader().loadTestsFromTestCase(module_12_3.RunnerTest))
calcST.addTest(unittest.TestLoader().loadTestsFromTestCase(module_12_3.TournamentTest))

runner: unittest.runner.TextTestRunner = unittest.TextTestRunner(verbosity=2)
runner.run(calcST)  # запуск тестов отдельного файла
