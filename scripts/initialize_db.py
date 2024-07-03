import sqlite3

def initialize_db(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Создание таблицы для исходных текстов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS texts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        cleaned_text TEXT
    )
    ''')

    # Создание таблиц для тренировочных и тестовых данных
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS train_texts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS test_texts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_db('db/database.db')
