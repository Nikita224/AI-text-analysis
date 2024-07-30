import sqlite3
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout

def load_data(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute('SELECT text FROM train_texts')
    train_texts = [row[0] for row in cursor.fetchall()]

    cursor.execute('SELECT text FROM test_texts')
    test_texts = [row[0] for row in cursor.fetchall()]

    conn.close()
    return train_texts, test_texts

def train_model(train_texts, test_texts, vocab_size=5000, max_length=100):
    # Проверка данных на пустые строки
    print("Количество тренировочных текстов:", len(train_texts))
    print("Количество тестовых текстов:", len(test_texts))
    
    if not train_texts or not test_texts:
        raise ValueError("Тренировочные или тестовые данные пусты.")
    
    tokenizer = Tokenizer(num_words=vocab_size, oov_token="<OOV>")
    tokenizer.fit_on_texts(train_texts)
    train_sequences = tokenizer.texts_to_sequences(train_texts)
    test_sequences = tokenizer.texts_to_sequences(test_texts)

    # Проверка последовательностей на пустые элементы
    if any(len(seq) == 0 for seq in train_sequences):
        raise ValueError("Найдены пустые последовательности в тренировочных данных.")
    if any(len(seq) == 0 for seq in test_sequences):
        raise ValueError("Найдены пустые последовательности в тестовых данных.")
    
    train_padded = pad_sequences(train_sequences, maxlen=max_length, padding='post', truncating='post')
    test_padded = pad_sequences(test_sequences, maxlen=max_length, padding='post', truncating='post')

    model = Sequential([
        Embedding(vocab_size, 64, input_length=max_length),
        LSTM(64, return_sequences=True),
        Dropout(0.5),
        LSTM(64),
        Dropout(0.5),
        Dense(32, activation='relu'),
        Dense(1, activation='sigmoid')
    ])

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.summary()

    model.fit(train_padded, epochs=5, validation_data=(test_padded))
    model.save('models/text_classification_model.h5')

if __name__ == '__main__':
    train_texts, test_texts = load_data('db/database.db')
    train_model(train_texts, test_texts)
