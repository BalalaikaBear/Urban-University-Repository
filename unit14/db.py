import random
import sqlite3

connection: sqlite3.Connection = sqlite3.connect('database.db')  # обращение к базе данных
cursor: sqlite3.Cursor = connection.cursor()

# Все ключевые команды пишутся КАПСОМ
# Все имена объектов пишутся с Заглавной Буквы
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER
)
''')
cursor.execute(' CREATE INDEX IF NOT EXISTS idx_email ON Users (email)')

# команды
# SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY

# ОСНОВНЫЕ ОПЕРАЦИИ ------------------------------------------------------------------------------------------------- *
# добавление данных в файл db
# ДОБАВИТЬ В ТАБЛИЦУ [Имя таблицы] ЗНАЧЕНИЯ [Username, Email, Age]
if False is True:
    cursor.execute('INSERT INTO Users (username, email, age) VALUES (?, ?, ?)',
                   ('Anton', 'ex@gmail.com', '22'))

if False is True:
    for i in range(20):
        cursor.execute('INSERT INTO Users (username, email, age) VALUES (?, ?, ?)',
                       (f'Username_{i}', f'ex{i}@gmail.com', str(random.randint(20, 60))))

# изменение данных
# ОБНОВИТЬ [Имя таблицы], УСТАНОВИТЬ [Возраст] = ? ГДЕ ИМЯ ПОЛЬЗОВАТЕЛЯ = ?
if False is True:
    cursor.execute('UPDATE Users SET age = ? WHERE username = ?',
                   (35, 'Anton'))

# удаление данных
# УДАЛИ ИЗ ТАБЛИЦЫ [Имя таблицы] ДАННЫЕ, ГДЕ ИПЯ ПОЛЬЗВАТЕЛЯ = ?
if False is True:
    cursor.execute('DELETE FROM Users WHERE username = ?', ('Anton', ))

# ПОЛУЧЕНИЕ ДАННЫХ ИЗ ТАБЛИЦЫ --------------------------------------------------------------------------------------- *
# получить все данные из таблицы
# ВЫБРАТЬ [Все поля] ИЗ ТАБЛИЦЫ [Имя таблицы]
cursor.execute('SELECT * FROM Users')
users: list[tuple] = cursor.fetchall()
for user in users:
    print("1:", user)

# получить указанные данные из таблицы
# ВЫБРАТЬ [Username, Age] ИЗ ТАБЛИЦЫ [Имя таблицы] ГДЕ [Возраст] > 35
cursor.execute('SELECT username, age FROM Users WHERE age > ?',
               (35, ))
users: list[tuple] = cursor.fetchall()
for user in users:
    print("2:", user)

# ВЫБРАТЬ [Username, age] ИЗ ТАБЛИЦЫ [Имя таблицы] И ОТСОРТИРОВАТЬ ПО [Возрасту]
cursor.execute('SELECT username, age, AVG(age) FROM Users GROUP BY age')
users: list[tuple] = cursor.fetchall()
for user in users:
    print("3:", user)

# получить кол-во пользователей из базы данных [COUNT]
# ВЫБРАТЬ/ВЕРНУТЬ КОЛ-ВО ДАННЫХ ИЗ ТАБЛИЦЫ [Имя таблицы], В КОТОРЫХ [Возраст] > 40
cursor.execute('SELECT COUNT(*) FROM Users WHERE age > ?',
               (40, ))
total: int = cursor.fetchone()[0]  # позволяет получить единичные данные
print("4:", total)

# получить сумму, среднее, минимальное и максимальное значения
# ВЫБРАТЬ/ВЕРНУТЬ СУММУ[Возраст], СРЕДНЕЕ[Возраст], МИН[Возраст] и МАКС[Возраст] ИЗ ТАБЛИЦЫ [Имя таблицы]
cursor.execute('SELECT SUM(age), AVG(age), MIN(age), MAX(age) FROM Users')
total: tuple = cursor.fetchone()
print("4:", total)

connection.commit()  # закрытие подключение
connection.close()  # запоминание состояния
