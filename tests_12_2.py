from runner_and_tournament import Runner, Tournament
import unittest


class TournamentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.all_results = {}

    def setUp(self) -> None:
        self.usain = Runner('Усэйн', 10)
        self.andrey = Runner('Андрей', 9)
        self.nick = Runner('Ник', 3)

    @classmethod
    def tearDownClass(cls) -> None:
        for test_name, result in cls.all_results.items():
            formatted_results = {place: str(runner) for place, runner in
                                 result.items()}
            print(formatted_results)

    def test_usain_and_nick(self) -> None:
        tournament = Tournament(90, self.usain, self.nick)
        result = tournament.start()
        self.all_results['test_usain_and_nick'] = result
        self.assertTrue(str(result[max(result.keys())]) == 'Ник')

    def test_andrey_and_nick(self) -> None:
        tournament = Tournament(90, self.andrey, self.nick)
        result = tournament.start()
        self.all_results['test_andrey_and_nick'] = result
        self.assertTrue(str(result[max(result.keys())]) == 'Ник')

    def test_usain_andrey_and_nick(self) -> None:
        tournament = Tournament(90, self.usain, self.andrey, self.nick)
        result = tournament.start()
        self.all_results['test_usain_andrey_and_nick'] = result
        self.assertTrue(str(result[max(result.keys())]) == 'Ник')


if __name__ == '__main__':
    unittest.main()
