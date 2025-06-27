from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import Any

class RecommendationEngine:
    def __init__(self, vectorizer=None):
        self.vectorizer = vectorizer or TfidfVectorizer()
        self.anchor_vector = None

    def train(self, anchor_text: str, articles: list[dict[str, Any]]):
        """Training the model on given anchor text and articles"""
        # Creating a single corpus from existing articles
        corpus = [anchor_text] + [art['content'] for art in articles]
        
        # Vectorization
        tfidf_matrix = self.vectorizer.fit_transform(corpus)
        
        # Saving anchor vector
        self.anchor_vector = tfidf_matrix[0]
        self.article_vectors = tfidf_matrix[1:]

    def recommend(self, articles: list[dict[str, Any]], top_n: int = 5) -> list[dict[str, Any]]:
        """Organizes articles by rating"""
        similarities = linear_kernel(self.anchor_vector, self.article_vectors)[0]
        
        sorted_indices = similarities.argsort()[::-1]
        recommendations = []
        for idx in sorted_indices[:top_n]:
            articles[idx]['similarity'] = float(similarities[idx])
            recommendations.append(articles[idx])
            
        return recommendations