from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

import logging
logger = logging.getLogger(__name__)

from typing import Any

class RecommendationEngine:
    def __init__(self, vectorizer=None, model=None):
        self.vectorizer = vectorizer or TfidfVectorizer()
        self.anchor_vector = None

    # TODO: word2vec instead of TF-IDF
    def train(self, anchor_text: str, articles: list[dict[str, Any]]):
        """Training the model on given anchor text and articles"""
        # Creating a single corpus from existing articles
        corpus = [anchor_text] + [art['content'] for art in articles]
        
        # Vectorization
        try:
            tfidf_matrix = self.vectorizer.fit_transform(corpus)
        except ValueError as e:
            logger.error("Corpus can't be vectorized: %s", str(e), exc_info=True)
            raise ValueError(f"Corpus can't be vectorized: {str(e)}") from e
        
        # Saving anchor vector
        self.anchor_vector = tfidf_matrix[0]
        self.article_vectors = tfidf_matrix[1:]

    def recommend(self, articles: list[dict[str, Any]], top_n: int = 5) -> list[dict[str, Any]]:
        """Organizes articles by rating"""
        similarities = cosine_similarity(self.anchor_vector, self.article_vectors)[0]
        
        sorted_indices = similarities.argsort()[::-1]
        recommendations = []
        for idx in sorted_indices[:top_n]:
            articles[idx]['similarity'] = float(similarities[idx])
            recommendations.append(articles[idx])
            
        return recommendations