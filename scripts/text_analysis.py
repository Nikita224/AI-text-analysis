import sqlite3
from collections import Counter

def analyze_text(db_file):
    # Подключение к базе данных
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Извлечение предобработанных текстов
    cursor.execute('SELECT cleaned_text FROM texts')
    rows = cursor.fetchall()
    all_text = ' '.join([row[0] for row in rows if row[0] is not None])

    # Подсчет частоты слов
    word_counts = Counter(all_text.split())

    # Закрытие соединения
    conn.close()

    return word_counts

if __name__ == '__main__':
    word_counts = analyze_text('db/database.db')
    print(word_counts.most_common(10))
