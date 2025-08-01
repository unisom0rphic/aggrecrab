import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from typing import Any

import logging
logger = logging.getLogger(__name__)

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
        
        # Normalization
        # 1e-8 = 10^(-8) to avoid division by zero
        similarities = (similarities - similarities.min()) / (similarities.max() - similarities.min() + 1e-8)
        
        logger.info(
            "Similarity statistics: Max=%.2f, Min=%.2f, Avg=%.2f",
            max(similarities),
            min(similarities),
            sum(similarities)/len(similarities)
        )
        
        
        sorted_indices = similarities.argsort()[::-1]
        recommendations = [{
            **articles[idx],
            'similarity': f"{similarities[idx]*100:.2f}%"
        } for idx in sorted_indices[:top_n] if similarities[idx] > 0]

        return recommendations