import feedparser
import streamlit as st
import concurrent.futures
from typing import Any
from datetime import timedelta

class ArticleRetriever:
    @staticmethod
    @st.cache_data(ttl=timedelta(minutes=30))
    def fetch_all_feeds(rss_urls: list[str]) -> list:
        """Fetching articles from RSS feeds"""
        feed_articles = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Contains articles from different feeds separately
            feed_articles = list(executor.map(ArticleRetriever._fetch_feed, rss_urls))  
        # Flattens the list to get all articles without feed separation
        return [art for feed in feed_articles for art in feed]

    @staticmethod
    def _fetch_feed(url) -> list:
        """Fetches one specific feed to allow multithreading"""
        feed_articles = []
        feed = feedparser.parse(url)
        for entry in feed.entries:
            content = getattr(entry, 'description', '') or getattr(entry, 'summary', '')
            feed_articles.append({
                'title': entry.title,
                'url': entry.link,
                'content': content,
                'source': url
            })
        return feed_articles