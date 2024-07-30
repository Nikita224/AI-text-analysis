import matplotlib.pyplot as plt
from scripts.text_analysis import analyze_text

def visualize_word_counts(word_counts):
    words, counts = zip(*word_counts.most_common(10))

    plt.figure(figsize=(10, 6))
    plt.bar(words, counts)
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title('Top 10 Words Frequency')
    plt.show()

if __name__ == '__main__':
    word_counts = analyze_text('db/database.db')
    visualize_word_counts(word_counts)
