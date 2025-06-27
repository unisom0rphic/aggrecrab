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
