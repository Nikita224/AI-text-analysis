from scripts.initialize_db import initialize_db
from scripts.data_collection import load_data_to_db
from scripts.data_preprocessing import preprocess_data, split_data
from scripts.text_analysis import analyze_text
from scripts.visualization import visualize_word_counts
from scripts.text_classification import train_model, load_data as load_train_test_data
from scripts.sentiment_analysis import analyze_sentiments, load_data as load_all_texts

if __name__ == '__main__':
    # Инициализация базы данных
    initialize_db('db/database.db')
    
    # Сбор данных
    load_data_to_db('data/texts.csv', 'db/database.db')
    
    # Предобработка данных
    preprocess_data('db/database.db')
    split_data('db/database.db')
    
    # Анализ текста
    word_counts = analyze_text('db/database.db')
    visualize_word_counts(word_counts)
    
    # Классификация текста
    train_texts, test_texts = load_train_test_data('db/database.db')
    train_model(train_texts, test_texts)
    
    # Анализ настроений
    texts = load_all_texts('db/database.db')
    sentiments = analyze_sentiments(texts, 'models/text_classification_model.h5')
    print(sentiments[:10])  # Вывод первых 10 результатов
