import sqlite3
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from sklearn.model_selection import train_test_split

# Скачивание необходимых ресурсов NLTK
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
    for row in rows:
        cleaned_text = preprocess_text(row[1])
        cursor.execute('UPDATE texts SET cleaned_text = ? WHERE id = ?', (cleaned_text, row[0]))

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()

def split_data(db_file, test_size=0.2):
    # Подключение к базе данных
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Извлечение предобработанных текстов
    cursor.execute('SELECT cleaned_text FROM texts')
    rows = cursor.fetchall()
    texts = [row[0] for row in rows if row[0] is not None]

    # Разделение данных на тренировочные и тестовые
    train_texts, test_texts = train_test_split(texts, test_size=test_size)

    # Очистка старых данных и вставка новых
    cursor.execute('DELETE FROM train_texts')
    cursor.execute('DELETE FROM test_texts')

    for text in train_texts:
        cursor.execute('INSERT INTO train_texts (text) VALUES (?)', (text,))
    
    for text in test_texts:
        cursor.execute('INSERT INTO test_texts (text) VALUES (?)', (text,))

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()

if __name__ == '__main__':
    preprocess_data('db/database.db')
    split_data('db/database.db')
