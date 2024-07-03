import sqlite3
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

nltk.download('stopwords')
nltk.download('punkt')

def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    filtered_tokens = [word for word in tokens if word not in stopwords.words('english')]
    return ' '.join(filtered_tokens)

def preprocess_data(db_file):
    # Подключение к базе данных
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Извлечение текстов и предобработка
    cursor.execute('SELECT id, text FROM texts')
    rows = cursor.fetchall()
    print(f"Количество текстов для предобработки: {len(rows)}")
    for row in rows:
        cleaned_text = preprocess_text(row[1])
        cursor.execute('UPDATE texts SET cleaned_text = ? WHERE id = ?', (cleaned_text, row[0]))

    # Извлечение текстов авторов и предобработка
    cursor.execute('SELECT id, text FROM authors')
    rows = cursor.fetchall()
    print(f"Количество текстов авторов для предобработки: {len(rows)}")
    for row in rows:
        cleaned_text = preprocess_text(row[1])
        cursor.execute('UPDATE authors SET cleaned_text = ? WHERE id = ?', (cleaned_text, row[0]))

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()

if __name__ == '__main__':
    preprocess_data('db/database.db')
