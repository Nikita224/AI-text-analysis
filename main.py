from scripts.initialize_db import initialize_db, extract_data, load_authors_to_db
from scripts.data_collection import load_data_to_db
from scripts.data_preprocessing import preprocess_data
from scripts.text_analysis import analyze_text
from scripts.visualization import visualize_word_counts
from scripts.train_model import load_author_data, train_author_model
from scripts.predict_author import predict_author
import os

def main():
    db_file = 'db/database.db'
    source_db_file = 'data/PubMedArticles-7.db'
    data_csv_file = 'data/texts.csv'

    print("Выберите действие:")
    print("1. Анализ частоты слов")
    print("2. Классификация авторов")

    choice = input("Введите номер действия (1 или 2): ")

    if choice == "1":
        # Инициализация базы данных
        initialize_db(db_file)
        
        # Сбор данных
        if os.path.exists(data_csv_file):
            load_data_to_db(data_csv_file, db_file)
        else:
            print(f"Файл {data_csv_file} не найден.")
        
        # Предобработка данных
        preprocess_data(db_file)
        
        # Анализ текста
        word_counts = analyze_text(db_file)
        visualize_word_counts(word_counts)

    elif choice == "2":
        # Инициализация базы данных
        initialize_db(db_file)
        
        # Извлечение и загрузка данных авторов
        data = extract_data(source_db_file)
        load_authors_to_db(data, db_file)
        
        # Предобработка данных
        preprocess_data(db_file)
        
        # Обучение модели классификации авторов
        author_data = load_author_data(db_file)
        train_author_model(author_data)
        
        # Предсказание автора нового текста
        new_text = input("Введите текст для предсказания автора: ")
        author = predict_author(new_text)
        print(f"Предсказанный автор: {author}")
    
    else:
        print("Неверный выбор. Пожалуйста, введите 1 или 2.")

if __name__ == '__main__':
    main()
