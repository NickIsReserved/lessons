import unittest
import logging
from rt_with_exceptions import Runner

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    filename='runner_tests.log',
    filemode='w',
    encoding='utf-8',
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class RunnerTest(unittest.TestCase):

    def test_walk(self):
        try:
            # Создание объекта Runner с некорректной скоростью
            runner = Runner("Test Runner", speed=-5)
        except ValueError as e:
            # Логирование ошибки на уровне WARNING
            logging.warning("Неверная скорость для Runner: %s", str(e))
        else:
            for _ in range(10):
                runner.walk()
            self.assertEqual(runner.distance, 50)
            # Логирование успешного выполнения теста
            logging.info('"test_walk" выполнен успешно')

    def test_run(self):
        try:
            # Создание объекта Runner с некорректным типом имени
            runner = Runner(12345)
        except TypeError as e:
            # Логирование ошибки на уровне WARNING
            logging.warning("Неверный тип данных для объекта Runner: %s",
                            str(e))
        else:
            for _ in range(10):
                runner.run()
            self.assertEqual(runner.distance, 100)
            # Логирование успешного выполнения теста
            logging.info('"test_run" выполнен успешно')

    def test_challenge(self):
        # Создание корректных объектов Runner
        runner1 = Runner("Runner 1")
        runner2 = Runner("Runner 2")
        # Проверка разницы в пройденной дистанции между бегунами
        for _ in range(10):
            runner1.run()
            runner2.walk()
        self.assertNotEqual(runner1.distance, runner2.distance)
        # Логирование успешного выполнения теста
        logging.info('"test_challenge" выполнен успешно')


if __name__ == '__main__':
    unittest.main()
