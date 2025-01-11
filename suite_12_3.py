import unittest
from tests_12_3 import RunnerTest, TournamentTest

# Создаём объект TestSuite
suite = unittest.TestSuite()

# Добавляем тесты из RunnerTest
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(RunnerTest))

# Добавляем тесты из TournamentTest
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TournamentTest))

# Создаём объект TextTestRunner с verbosity=2
runner = unittest.TextTestRunner(verbosity=2)

if __name__ == "__main__":
    runner.run(suite)
