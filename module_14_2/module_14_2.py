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

for i in range(1, 11):
    cursor.execute(
        'INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
        (f'User{i}', f'example{i}@gmail.com', f'{i * 10}', 1000))

cursor.execute('UPDATE Users SET balance = 500 WHERE id % 2 = 1')

cursor.execute('DELETE FROM Users WHERE id % 3 = 1')

# Удаление записи с id = 6
cursor.execute('DELETE FROM Users WHERE id = 6')

# Подсчет общего количества записей
cursor.execute('SELECT COUNT(*) FROM Users')
total_records = cursor.fetchone()[0]

# Подсчет суммы всех балансов
cursor.execute('SELECT SUM(balance) FROM Users')
total_balance = cursor.fetchone()[0]

# Вычисление среднего баланса всех пользователей
"""
Использование функции AVG
cursor.execute('SELECT AVG(balance) FROM Users')
average_balance = cursor.fetchone()[0]
print(average_balance)
"""
print(total_balance / total_records)

connection.commit()
connection.close()
