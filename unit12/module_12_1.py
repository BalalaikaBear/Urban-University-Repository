import runner
import unittest

type Runner = runner.Runner

class RunnerTest(unittest.TestCase):
    def test_wall(self) -> None:
        obj: Runner = runner.Runner('name')
        for _ in range(10):
            obj.walk()
        self.assertEqual(obj.distance, 50)

    def test_run(self) -> None:
        obj: Runner = runner.Runner('name2')
        for _ in range(10):
            obj.run()
        self.assertEqual(obj.distance, 100)

    def test_challenge(self) -> None:
        obj_a: Runner = runner.Runner('Alfred')
        obj_b: Runner = runner.Runner('Billy')
        for _ in range(10):
            obj_a.walk()
            obj_b.run()
        self.assertNotEqual(obj_a.distance, obj_b.distance)

if __name__ == '__main__':
    unittest.main()
