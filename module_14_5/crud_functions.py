import sqlite3
from typing import List

DATABASE_FILE = "telegram_14_5.db"

def initiate_db() -> None:
    """
    Создаём таблицы Products, Users, если они еще не созданы.
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

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER NOT NULL,
            balance INTEGER NOT NULL
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


def add_user(username: str, email: str, age: int) -> None:
    """
    Добавляем нового пользователя в таблицу Users.
    """
    try:
        connection = sqlite3.connect(DATABASE_FILE)
        cursor = connection.cursor()

        cursor.execute('''
        INSERT INTO Users (username, email, age, balance)
        VALUES (?, ?, ?, ?);
        ''', (username, email, age, 1000))

        connection.commit()
        connection.close()
        print(f"Пользователь {username} успешно добавлен.")

    except sqlite3.Error as e:
        print(f"Ошибка при добавлении пользователя: {e}")


def is_included(username: str) -> bool:
    """
    Проверяем, существует ли пользователь с указанным именем в таблице Users.
    """
    try:
        connection = sqlite3.connect(DATABASE_FILE)
        cursor = connection.cursor()

        cursor.execute('''
        SELECT id FROM Users WHERE username = ?;
        ''', (username,))

        result = cursor.fetchone()

        connection.close()

        return result is not None

    except sqlite3.Error as e:
        print(f"Ошибка при поиске пользователя: {e}")
        return False


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


# fill_products()
