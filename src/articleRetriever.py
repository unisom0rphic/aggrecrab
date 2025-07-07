import feedparser
from typing import Any

class ArticleRetriever:
    @staticmethod
    def fetch_articles(rss_urls: list[str]) -> list[dict[str, Any]]:
        """Fetching articles from RSS feeds"""
        articles = []
        ENTRIES_LIMIT = 10
        for url in rss_urls:
            feed = feedparser.parse(url)
            for entry in feed.entries[:ENTRIES_LIMIT]:
                content = getattr(entry, 'description', '') or getattr(entry, 'summary', '')
                articles.append({
                    'title': entry.title,
                    'url': entry.link,
                    'content': content,
                    'source': url
                })
        return articles