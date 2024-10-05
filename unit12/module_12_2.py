import runner_and_tournament
import unittest

type Runner = runner_and_tournament.Runner
type Tournament = runner_and_tournament.Tournament

class TournamentTest(unittest.TestCase):
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

    def test_start_1(self) -> None:
        self.tournament: Tournament = runner_and_tournament.Tournament(
            90, self.runner_y, self.runner_n)
        self.all_results.append(self.tournament.start())
        last_result: dict[int: Runner] = self.all_results[-1]

        self.assertEqual(last_result[max(last_result)], 'Ник')

    def test_start_2(self) -> None:
        self.tournament: Tournament = runner_and_tournament.Tournament(
            90, self.runner_a, self.runner_n)
        self.all_results.append(self.tournament.start())
        last_result = self.all_results[-1]

        self.assertEqual(last_result[max(last_result)], 'Ник')

    def test_start_3(self) -> None:
        self.tournament: Tournament = runner_and_tournament.Tournament(
            90, self.runner_y, self.runner_a, self.runner_n)
        self.all_results.append(self.tournament.start())
        last_result = self.all_results[-1]

        self.assertEqual(last_result[max(last_result)], 'Ник')

if __name__ == '__main__':
    unittest.main()
