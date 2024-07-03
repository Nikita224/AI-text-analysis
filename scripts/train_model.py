from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn import metrics
import joblib
import sqlite3
import pandas as pd

def load_author_data(db_file):
    conn = sqlite3.connect(db_file)
    query = "SELECT author, cleaned_text FROM authors WHERE cleaned_text IS NOT NULL"
    data = pd.read_sql_query(query, conn)
    conn.close()
    print(f"Загружено {len(data)} записей авторов для обучения.")
    return data

def train_author_model(data):
    X = data['cleaned_text']
    y = data['author']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = make_pipeline(CountVectorizer(), MultinomialNB())
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(metrics.classification_report(y_test, y_pred))

    joblib.dump(model, 'models/author_classifier.pkl')

if __name__ == '__main__':
    data = load_author_data('db/database.db')
    train_author_model(data)
