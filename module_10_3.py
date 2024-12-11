import threading
import random
import time


class Bank:
    def __init__(self):
        self.balance: int = 0  # Начальный баланс
        self.lock = threading.Lock()  # Замок для синхронизации потоков

    def deposit(self):
        """Метод пополнения баланса."""
        for _ in range(100):
            amount = random.randint(50, 500)  # Случайная сумма пополнения
            with self.lock:  # блок with с замком lock
                self.balance += amount
                print(f"Пополнение: {amount}. Баланс: {self.balance}")

            if self.balance >= 500:
                # Попытка освободить lock только если он заблокирован
                try:
                    self.lock.release()
                except RuntimeError:
                    pass  # Игнорируем ошибку, если lock не был заблокирован

            time.sleep(0.001)

    def take(self):
        """Метод снятия с баланса."""
        for _ in range(100):
            amount = random.randint(50, 500)  # Случайная сумма снятия
            print(f"Запрос на {amount}")
            with self.lock:
                if amount <= self.balance:
                    self.balance -= amount
                    print(f"Снятие: {amount}. Баланс: {self.balance}")
                else:
                    print("Запрос отклонён, недостаточно средств")
                    # Блокируем lock только внутри блока with
                    self.lock.acquire(blocking=False)

            time.sleep(0.001)


bk = Bank()

# Создаем потоки для пополнения и снятия
th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

# Запускаем потоки
th1.start()
th2.start()

# Ожидаем завершения потоков
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
