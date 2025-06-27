from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import string

class TextPreprocessor:
    def __init__(self, language: str = "russian"):
        self.language = language
        self.stop_words = set(stopwords.words(language))
        self.stemmer = SnowballStemmer(language)
        self.punctuation = string.punctuation + "«»“”…–"

    def preprocess(self, text: str) -> str:
        """Очистка и нормализация текста"""
        text = text.lower()
        # Удаление пунктуации
        text = text.translate(str.maketrans('', '', self.punctuation))
        # Токенизация и обработка
        tokens = []
        for token in text.split():
            if token not in self.stop_words and len(token) > 2:
                tokens.append(self.stemmer.stem(token))
        return " ".join(tokens)