import sqlite3

connection: sqlite3.Connection = sqlite3.connect('not_telegram.db')  # обращение к базе данных
cursor: sqlite3.Cursor = connection.cursor()

# Все ключевые команды пишутся КАПСОМ
# Все имена объектов пишутся с Заглавной Буквы
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

# добавление данных в файл db
for i in range(1, 11):
    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
                   (f'User{i}', f'example{i}@gmail.com', str(i*10), '1000'))

# обновление данных
for i in range(2, 11, 2):
    cursor.execute('UPDATE Users SET balance = 500 WHERE username = ?',
                   (f'User{i}', ))

# удаление данных
for i in range(1, 11, 3):
    cursor.execute('DELETE FROM Users WHERE username = ?',
                   (f'User{i}', ))

# получить указанные данные из таблицы
cursor.execute('SELECT username, email, age, balance FROM Users WHERE age != 60')
data: list[tuple] = cursor.fetchall()
for line in data:
    print('Имя:', line)
