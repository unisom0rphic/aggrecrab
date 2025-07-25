import yaml
from typing import Any, Optional

from textPreprocessor import TextPreprocessor
from articleRetriever import ArticleRetriever
from enhancedRecommendEngine import EnhancedRecommendationEngine

import logging
logger = logging.getLogger(__name__)

class ArticleRecommender:
    def __init__(self, request: str, config_path: str="config.yaml"):
        self.request = request
        self.config = self._load_config(config_path)
        self.preprocessor = TextPreprocessor()
        self.retriever = ArticleRetriever()
        self.engine = EnhancedRecommendationEngine()

    @staticmethod
    def _load_config(path: str) -> dict:
        try:
            logger.debug("Loading config from: %s", path)
            with open(path, 'r') as f:
                config = yaml.safe_load(f)
            logger.info("Successfully loaded config from: %s", path)
            return config
        except FileNotFoundError:
            logger.error("Config file not found: %s", path, exc_info=True)
            raise
        except yaml.YAMLError as e:
            logger.error("Invalid YAML in config file: %s", path, exc_info=True)
            raise ValueError(f"Invalid YAML in {path}") from e


    def run(self) -> list[dict[str, Any]]:
        """Recommendations pipeline"""
        # Downloading and preprocessing
        anchor_text = self.request or self.preprocessor.preprocess(self.config['anchor_text'])
        
        # Retrieving articles
        articles = self.retriever.fetch_all_feeds(self.config['sources'])
        
        # Preprocessing articles text
        for art in articles:
            art['processed_content'] = self.preprocessor.preprocess(art['content'])
        
        # Training and receiving recommendations
        self.engine.train(anchor_text, articles)
        return self.engine.recommend(articles, top_n=self.config.get('top_n', 5))
