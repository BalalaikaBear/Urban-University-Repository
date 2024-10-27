import sqlite3

connection: sqlite3.Connection = sqlite3.connect('products.db')  # обращение к базе данных
cursor: sqlite3.Cursor = connection.cursor()

def initiate_db(stop_connect: bool = True) -> None:
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    ''')
    if stop_connect:
        connection.commit()  # закрытие подключения
        connection.close()  # запоминание состояния

def get_all_products() -> list[tuple]:
    cursor.execute('SELECT * FROM Users')
    return cursor.fetchall()

def create_db() -> None:
    for i in range(1, 5):
        cursor.execute(f'INSERT INTO Users VALUES ("{i}", "Продукт {i}", "Описание {i}", "{i * 100}")')
    connection.commit()  # закрытие подключения
    connection.close()  # запоминание состояния

if __name__ == '__main__':
    initiate_db(False)
    create_db()

