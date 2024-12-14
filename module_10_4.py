import threading
import time
import random
from queue import Queue
from typing import List


class Table:
    """Класс для представления стола в кафе."""

    def __init__(self, number: int) -> None:
        self.number = number
        self.guest: Guest | None = None  # Гость, сидящий за столом (изначально None)


class Guest(threading.Thread):
    """Класс для представления гостя как потока."""

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

    def run(self) -> None:
        """Имитирует время пребывания гостя за столом."""
        eating_time = random.randint(3, 10)  # Случайное время 3-10 сек
        time.sleep(eating_time)


class Cafe:
    """Класс для представления кафе с гостями и столами."""

    def __init__(self, *tables: Table) -> None:
        self.tables: List[Table] = list(tables)  # Список столов
        self.queue: Queue[Guest] = Queue()  # Очередь гостей (потоков)

    def guest_arrival(self, *guests: Guest) -> None:
        """Метод прибытия гостей в кафе."""
        for guest in guests:
            # Ищем свободный стол
            free_table = next(
                (table for table in self.tables if table.guest is None), None)
            if free_table:  # Если есть свободный стол
                free_table.guest = guest  # Сажаем гостя за стол
                guest.start()  # Запускаем поток гостя
                print(
                    f"{guest.name} сел(-а) за стол номер {free_table.number}")
            else:  # Если столов нет, ставим гостя в очередь
                self.queue.put(guest)
                print(f"{guest.name} в очереди")

    def discuss_guests(self) -> None:
        """Метод обслуживания гостей."""
        while not self.queue.empty() or any(
                table.guest for table in self.tables):
            for table in self.tables:
                # Проверяем, не исполняется ли поток. Метод is_alive()
                if table.guest and not table.guest.is_alive():  # Гость закончил еду
                    print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")
                    print(f"Стол номер {table.number} свободен")
                    table.guest = None  # Освобождаем стол

                if table.guest is None and not self.queue.empty():  # Если стол свободен...
                    next_guest = self.queue.get()  # Берем следующего гостя из очереди
                    table.guest = next_guest  # Сажаем за стол
                    next_guest.start()  # Запускаем поток гостя
                    print(
                        f"{next_guest.name} вышел(-ла) из очереди и сел(-а) "
                        f"за стол номер {table.number}")


# Создание столов
tables = [Table(number) for number in range(1, 6)]

# Имена гостей
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]

# Создание гостей
guests = [Guest(name) for name in guests_names]

# Заполнение кафе столами
cafe = Cafe(*tables)

# Приём гостей
cafe.guest_arrival(*guests)

# Обслуживание гостей
cafe.discuss_guests()
