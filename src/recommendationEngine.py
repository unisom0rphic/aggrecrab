from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import Any

class RecommendationEngine:
    def __init__(self, vectorizer=None):
        self.vectorizer = vectorizer or TfidfVectorizer()
        self.anchor_vector = None

    def train(self, anchor_text: str, articles: list[dict[str, Any]]):
        """Обучение модели на опорном тексте и статьях"""
        # Преобразование текстов в единый корпус
        corpus = [anchor_text] + [art['content'] for art in articles]
        
        # Векторизация
        tfidf_matrix = self.vectorizer.fit_transform(corpus)
        
        # Сохраняем вектор опорного текста (первый в матрице)
        self.anchor_vector = tfidf_matrix[0]
        self.article_vectors = tfidf_matrix[1:]

    def recommend(self, articles: list[dict[str, Any]], top_n: int = 5) -> list[dict[str, Any]]:
        """Ранжирование статей по релевантности"""
        similarities = linear_kernel(self.anchor_vector, self.article_vectors)[0]
        
        # Сортировка по релевантности
        sorted_indices = similarities.argsort()[::-1]
        recommendations = []
        for idx in sorted_indices[:top_n]:
            articles[idx]['similarity'] = float(similarities[idx])
            recommendations.append(articles[idx])
            
        return recommendations