import runner_and_tournament
import runner
import unittest

type Runner = runner_and_tournament.Runner
type Tournament = runner_and_tournament.Tournament

class TournamentTest(unittest.TestCase):
    is_frozen = True

    def setUp(self) -> None:
        self.runner_y: Runner = runner_and_tournament.Runner('Усейн', speed=10)
        self.runner_a: Runner = runner_and_tournament.Runner('Андрей', speed=9)
        self.runner_n: Runner = runner_and_tournament.Runner('Ник', speed=3)

    @classmethod
    def setUpClass(cls) -> None:
        cls.all_results: list = []

    @classmethod
    def tearDownClass(cls) -> None:
        for result in cls.all_results:
            print(result)

    @unittest.skipIf(is_frozen, 'Тесты в этом кейсе заморожены')
    def test_start_1(self) -> None:
        self.tournament: Tournament = runner_and_tournament.Tournament(
            90, self.runner_y, self.runner_n)
        self.all_results.append(self.tournament.start())
        last_result: dict[int: Runner] = self.all_results[-1]

        self.assertEqual(last_result[max(last_result)], 'Ник')

    @unittest.skipIf(is_frozen, 'Тесты в этом кейсе заморожены')
    def test_start_2(self) -> None:
        self.tournament: Tournament = runner_and_tournament.Tournament(
            90, self.runner_a, self.runner_n)
        self.all_results.append(self.tournament.start())
        last_result = self.all_results[-1]

        self.assertEqual(last_result[max(last_result)], 'Ник')

    @unittest.skipIf(is_frozen, 'Тесты в этом кейсе заморожены')
    def test_start_3(self) -> None:
        self.tournament: Tournament = runner_and_tournament.Tournament(
            90, self.runner_y, self.runner_a, self.runner_n)
        self.all_results.append(self.tournament.start())
        last_result = self.all_results[-1]

        self.assertEqual(last_result[max(last_result)], 'Ник')


type Runner = runner.Runner

class RunnerTest(unittest.TestCase):
    is_frozen = False

    @unittest.skipIf(is_frozen, 'Тесты в этом кейсе заморожены')
    def test_wall(self) -> None:
        obj: Runner = runner.Runner('name')
        for _ in range(10):
            obj.walk()
        self.assertEqual(obj.distance, 50)

    @unittest.skipIf(is_frozen, 'Тесты в этом кейсе заморожены')
    def test_run(self) -> None:
        obj: Runner = runner.Runner('name2')
        for _ in range(10):
            obj.run()
        self.assertEqual(obj.distance, 100)

    @unittest.skipIf(is_frozen, 'Тесты в этом кейсе заморожены')
    def test_challenge(self) -> None:
        obj_a: Runner = runner.Runner('Alfred')
        obj_b: Runner = runner.Runner('Billy')
        for _ in range(10):
            obj_a.walk()
            obj_b.run()
        self.assertNotEqual(obj_a.distance, obj_b.distance)

if __name__ == '__main__':
    unittest.main()
