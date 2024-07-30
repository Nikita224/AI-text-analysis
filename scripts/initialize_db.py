import sqlite3
import pandas as pd

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

    # Создание таблицы для авторов и их текстов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS authors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        author TEXT NOT NULL,
        text TEXT NOT NULL,
        cleaned_text TEXT
    )
    ''')

    conn.commit()
    conn.close()

def extract_data(db_file):
    conn = sqlite3.connect(db_file)
    query = "SELECT Author as author, Abstract as text FROM ArticleStruct"  # Извлекаем данные из таблицы ArticleStruct
    data = pd.read_sql_query(query, conn)
    conn.close()
    print(f"Извлечено {len(data)} записей из базы данных.")
    return data

def load_authors_to_db(data, db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Очистка таблицы перед загрузкой данных
    cursor.execute('DELETE FROM authors')

    for _, row in data.iterrows():
        cursor.execute('INSERT INTO authors (author, text) VALUES (?, ?)', (row['author'], row['text']))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_db('db/database.db')
    data = extract_data('data/PubMedArticles-7.db')
    load_authors_to_db(data, 'db/database.db')
    print(data.head())
