import joblib
from scripts.data_preprocessing import preprocess_text

def predict_author(text, model_path='models/author_classifier.pkl'):
    model = joblib.load(model_path)
    cleaned_text = preprocess_text(text)
    prediction = model.predict([cleaned_text])
    return prediction[0]

if __name__ == '__main__':
    new_text = "Enter the new text here for which you want to predict the author."
    author = predict_author(new_text)
    print(f"The predicted author is: {author}")
