from runner_and_tournament import Runner, Tournament
import unittest


class TournamentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.all_results = {}

    def setUp(self) -> None:
        self.usain = Runner('Быстрый', 10)
        self.andrey = Runner('Средний', 7)
        self.nick = Runner('Медленный', 5)

    @classmethod
    def tearDownClass(cls) -> None:
        for key, value in cls.all_results.items():
            formatted_results = {place: str(runner) for place, runner in
                                 value.items()}
            print(formatted_results)

    def test_diff_speed_case(self):
        tournament = Tournament(30, self.usain, self.andrey, self.nick)
        result = tournament.start()
        self.all_results["Logic Error"] = result
        self.assertTrue(str(result[max(result.keys())]) == 'Медленный')


if __name__ == '__main__':
    unittest.main()
