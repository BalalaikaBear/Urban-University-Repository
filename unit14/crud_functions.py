import sqlite3

connection: sqlite3.Connection = sqlite3.connect('products.db')  # обращение к базе данных
cursor: sqlite3.Cursor = connection.cursor()

def initiate_db(stop_connect: bool = True) -> None:
    # таблица продуктов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    ''')
    # таблица пользователей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL
    )
    ''')
    if stop_connect:
        connection.commit()  # закрытие подключения
        connection.close()  # запоминание состояния

def get_all_products() -> list[tuple]:
    cursor.execute('SELECT * FROM Products')
    connection.commit()
    return cursor.fetchall()

def create_db() -> None:
    for i in range(1, 5):
        cursor.execute(f'INSERT INTO Products VALUES ("{i}", "Продукт {i}", "Описание {i}", "{i * 100}")')
    connection.commit()  # закрытие подключения

def add_user(username, email, age) -> None:
    if not is_included(username):
        cursor.execute(f'INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
                       (username, email, age, 1000))
        connection.commit()

def is_included(username) -> bool:
    cursor.execute(f'SELECT * FROM Users')
    users: list[tuple] = cursor.fetchall()
    for user in users:
        if user[1] == username:
            return True
    return False

if __name__ == '__main__':
    initiate_db(False)
    #create_db()
    add_user('Name', 'name@email.ru', 22)

