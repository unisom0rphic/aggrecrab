import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from typing import Any

from recommendationEngine import RecommendationEngine

class EnhancedRecommendationEngine(RecommendationEngine):
    def __init__(self):
        super().__init__(vectorizer=TfidfVectorizer(
            ngram_range=(1, 2),
            min_df=0.01,
            max_df=0.85,
            max_features=5000
        ))
    
    def recommend(self, articles: list[dict[str, Any]], top_n: int = 5) -> list[dict[str, Any]]:
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