import yaml
from typing import Any

from textPreprocessor import TextPreprocessor
from articleRetriever import ArticleRetriever
from enhancedRecommendEngine import EnhancedRecommendationEngine

class ArticleRecommender:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.preprocessor = TextPreprocessor()
        self.retriever = ArticleRetriever()
        self.engine = EnhancedRecommendationEngine()

    @staticmethod
    def _load_config(path: str) -> dict:
        with open(path, 'r') as f:
            return yaml.safe_load(f)

    def run(self) -> list[dict[str, Any]]:
        """Recommendations pipeline"""
        # Downloading and preprocessing
        anchor_text = self.preprocessor.preprocess(self.config['anchor_text'])
        
        # Retrieving articles
        articles = self.retriever.fetch_articles(self.config['sources'])
        
        # Preprocessing articles text
        for art in articles:
            art['processed_content'] = self.preprocessor.preprocess(art['content'])
        
        # Training and receiving recommendations
        self.engine.train(anchor_text, articles)
        return self.engine.recommend(articles, top_n=self.config.get('top_n', 5))
