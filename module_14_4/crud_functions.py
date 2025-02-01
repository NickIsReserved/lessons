import sqlite3
from typing import List

DATABASE_FILE = "not_telegram.db"

def initiate_db() -> None:
    """
    Создаём таблицу Products, если она еще не создана.
    """
    try:
        connection = sqlite3.connect(DATABASE_FILE)
        cursor = connection.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL
        );
        ''')

        connection.commit()
        connection.close()

    except sqlite3.Error as e:
        print(f"Ошибка при создании таблицы: {e}")


def get_all_products() -> List:
    """
    Возвращаем все записи из таблицы Products.
    """
    try:
        connection = sqlite3.connect(DATABASE_FILE)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Products;")

        products = cursor.fetchall()
        connection.close()

        return products

    except sqlite3.Error as e:
        print(f"Ошибка при получении данных: {e}")
        return []


def fill_products() -> None:
    """
    Заполняем таблицу Products.
    """
    try:
        connection = sqlite3.connect(DATABASE_FILE)
        cursor = connection.cursor()

        total_products = 4 # Количество Products

        for i in range(1, total_products + 1):
            cursor.execute(
                'INSERT INTO Products (id, title, description, price) VALUES (?, ?, ?, ?)',
                (f'{i}', f'Продукт {i}', f'Описание {i}', f'{i * 100}'))

        connection.commit()
        connection.close()
        print(f"Products успешно добавлены.")

    except sqlite3.Error as e:
        print(f"Ошибка при добавлении пользователя: {e}")


# initiate_db()
# fill_products()
# print(get_all_products())
