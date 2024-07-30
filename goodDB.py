import sqlite3

def check_data(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute('SELECT id, text FROM train_texts WHERE text IS NULL OR text = ""')
    empty_train_texts = cursor.fetchall()

    cursor.execute('SELECT id, text FROM test_texts WHERE text IS NULL OR text = ""')
    empty_test_texts = cursor.fetchall()

    conn.close()

    return empty_train_texts, empty_test_texts

if __name__ == '__main__':
    empty_train_texts, empty_test_texts = check_data('db/database.db')
    print("Пустые тренировочные тексты:", empty_train_texts)
    print("Пустые тестовые тексты:", empty_test_texts)
