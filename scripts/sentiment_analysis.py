import sqlite3
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

def load_data(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute('SELECT cleaned_text FROM texts')
    texts = [row[0] for row in cursor.fetchall()]

    conn.close()
    return texts

def analyze_sentiments(texts, model_path, vocab_size=5000, max_length=100):
    model = tf.keras.models.load_model(model_path)

    tokenizer = Tokenizer(num_words=vocab_size, oov_token="<OOV>")
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)
    padded = pad_sequences(sequences, maxlen=max_length, padding='post', truncating='post')

    predictions = model.predict(padded)
    sentiments = ["Positive" if pred > 0.5 else "Negative" for pred in predictions]
    return sentiments

if __name__ == '__main__':
    texts = load_data('db/database.db')
    sentiments = analyze_sentiments(texts, 'models/text_classification_model.h5')
    print(sentiments[:10])  # Вывод первых 10 результатов
