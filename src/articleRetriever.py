import feedparser
import streamlit as st
import concurrent.futures
from typing import Any
from datetime import timedelta

import logging
logger = logging.getLogger(__name__)

class RSSFetchError(Exception):
    pass

class ArticleRetriever:
    @staticmethod
    @st.cache_data(ttl=timedelta(minutes=30))
    def fetch_all_feeds(rss_urls: list[str]) -> list:
        """Fetching articles from RSS feeds"""
        feeds_articles = []

        if not rss_urls:
            logger.warning("RSS URLs is empty")
            return []

        try:
            logger.info("Loading RSS feeds from: %s", rss_urls)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Contains articles from different feeds as separate lists
                feeds_articles = list(executor.map(ArticleRetriever._fetch_feed, rss_urls))  
                logger.info("Successfully processed %d feeds containing %d total articles", 
                    len(feeds_articles),
                    sum(len(feed) for feed in feeds_articles))
        except concurrent.futures.TimeoutError as e:
            logger.error("concurrent.futures timeout!\nRSS URLs: %s", rss_urls, exc_info=True)
            raise RSSFetchError(f"Unable to fetch RSS URLs: {str(e)}") from e

        # Flattens the list to get all articles without feed separation
        return [art for feed in feeds_articles for art in feed]

    @staticmethod
    def _fetch_feed(url) -> list:
        """Fetches one specific feed to allow multithreading"""
        feed_articles = []
        logger.debug("Fetching feed from %s", url)

        try:
            feed = feedparser.parse(url)
            logger.info("Successfully fetched source: %s", url)
            for entry in feed.entries:
                content = getattr(entry, 'description', '') or getattr(entry, 'summary', '')
                feed_articles.append({
                    'title': entry.title,
                    'url': entry.link,
                    'content': content,
                    'source': url
                })
            return feed_articles
        except Exception as e:
            logger.error("Parsing error at %s", url, exc_info=True)
            raise RSSFetchError(f"Parsing error at {url}: {str(e)}") from e