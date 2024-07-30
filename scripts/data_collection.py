import pandas as pd
import sqlite3
import csv

def load_data_to_db(csv_file, db_file):
    try:
        # Загрузка данных из CSV файла
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader)
            data = [row for row in reader]

        # Проверка количества полей в каждой строке
        for i, row in enumerate(data):
            if len(row) != len(headers):
                raise ValueError(f'Ошибка в строке {i+2}: ожидается {len(headers)} полей, найдено {len(row)}')

        # Подключение к базе данных
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Вставка данных в таблицу
        for row in data:
            cursor.execute('INSERT INTO texts (text) VALUES (?)', (row[0],))

        # Сохранение изменений и закрытие соединения
        conn.commit()
        conn.close()

    except Exception as e:
        print(f'Ошибка при загрузке данных: {e}')

if __name__ == '__main__':
    load_data_to_db('data/texts.csv', 'db/database.db')
