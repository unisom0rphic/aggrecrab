import feedparser
import yaml
import string
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from typing import List, Dict, Any

# Инициализация NLP компонентов
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

class ArticleRetriever:
    @staticmethod
    def fetch_articles(rss_urls: List[str]) -> List[Dict[str, Any]]:
        """Загрузка статей из RSS-лент"""
        articles = []
        for url in rss_urls:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                content = getattr(entry, 'description', '') or getattr(entry, 'summary', '')
                articles.append({
                    'title': entry.title,
                    'url': entry.link,
                    'content': content,
                    'source': url
                })
        return articles

class RecommendationEngine:
    def __init__(self, vectorizer=None):
        self.vectorizer = vectorizer or TfidfVectorizer()
        self.anchor_vector = None

    def train(self, anchor_text: str, articles: List[Dict[str, Any]]):
        """Обучение модели на опорном тексте и статьях"""
        # Преобразование текстов в единый корпус
        corpus = [anchor_text] + [art['content'] for art in articles]
        
        # Векторизация
        tfidf_matrix = self.vectorizer.fit_transform(corpus)
        
        # Сохраняем вектор опорного текста (первый в матрице)
        self.anchor_vector = tfidf_matrix[0]
        self.article_vectors = tfidf_matrix[1:]

    def recommend(self, articles: List[Dict[str, Any]], top_n: int = 5) -> List[Dict[str, Any]]:
        """Ранжирование статей по релевантности"""
        similarities = linear_kernel(self.anchor_vector, self.article_vectors)[0]
        
        # Сортировка по релевантности
        sorted_indices = similarities.argsort()[::-1]
        recommendations = []
        for idx in sorted_indices[:top_n]:
            articles[idx]['similarity'] = float(similarities[idx])
            recommendations.append(articles[idx])
            
        return recommendations

class EnhancedRecommendationEngine(RecommendationEngine):
    def __init__(self):
        super().__init__(vectorizer=TfidfVectorizer(
            ngram_range=(1, 2),
            min_df=0.01,
            max_df=0.85,
            max_features=5000
        ))
    
    def recommend(self, articles: List[Dict[str, Any]], top_n: int = 5) -> List[Dict[str, Any]]:
        similarities = np.array(linear_kernel(self.anchor_vector, self.article_vectors)[0])
        
        # Нормализация к диапазону [0, 1]
        similarities = (similarities - similarities.min()) /  (similarities.max() - similarities.min())
        
        print(f"Статистика схожести: Max={max(similarities):.2f}, Min={min(similarities):.2f}, Avg={sum(similarities)/len(similarities):.2f}")
        
        sorted_indices = similarities.argsort()[::-1]
        recommendations = [{
            **articles[idx],
            'similarity': f"{similarities[idx]*100:.2f}%"
        } for idx in sorted_indices[:top_n] if similarities[idx] > 0]

        return recommendations

# Основной пайплайн (интегратор компонентов)
class ArticleRecommenderSystem:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.preprocessor = TextPreprocessor()
        self.retriever = ArticleRetriever()
        self.engine = EnhancedRecommendationEngine()

    @staticmethod
    def _load_config(path: str) -> dict:
        with open(path, 'r') as f:
            return yaml.safe_load(f)

    def run(self) -> List[Dict[str, Any]]:
        """Запуск пайплайна рекомендаций"""
        # Загрузка и предобработка опорного текста
        anchor_text = self.preprocessor.preprocess(self.config['anchor_text'])
        
        # Получение статей
        articles = self.retriever.fetch_articles(self.config['sources'])
        
        # Предобработка контента статей
        for art in articles:
            art['processed_content'] = self.preprocessor.preprocess(art['content'])
        
        # Обучение и получение рекомендаций
        self.engine.train(anchor_text, articles)
        return self.engine.recommend(articles, top_n=self.config.get('top_n', 5))

# Точка входа
if __name__ == "__main__":
    # Пример config.yaml:
    # sources:
    #   - "https://example1.com/rss"
    #   - "https://example2.com/rss"
    # anchor_text: "технологии искусственный интеллект python"
    # top_n: 10
    
    recommender = ArticleRecommenderSystem("config.yaml")
    results = recommender.run()
    
    print("Топ рекомендаций:")
    for i, art in enumerate(results, 1):
        print(f"{i}. {art['title']} (Сходство: {art['similarity']})")
        print(f"   Ссылка: {art['url']}")
        print()