import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER,
    balance INTEGER NOT NULL
);
''')

# Заполнение БД 10-ю записями
for i in range(1, 11):
    cursor.execute(
        'INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
        (f'User{i}', f'example{i}@gmail.com', f'{i * 10}', 1000))

# Обновление balance у каждой 2-ой записи начиная с 1-ой на 500
cursor.execute('UPDATE Users SET balance = 500 WHERE id % 2 = 1')

# Удаление каждой 3-ей записи в таблице начиная с 1-ой
cursor.execute('DELETE FROM Users WHERE id % 3 = 1')

# Выборка всех записей, где возраст не равен 60
cursor.execute(
    'SELECT username, email, age, balance FROM Users WHERE age != 60')
rows = cursor.fetchall()

# Вывод результатов в консоль
for row in rows:
    print(
        f"Имя: {row[0]} | Почта: {row[1]} | Возраст: {row[2]} | Баланс: {row[3]}")

connection.commit()
connection.close()
