import feedparser
import streamlit as st
import concurrent.futures
from typing import Any
from datetime import timedelta
from urllib.robotparser import RobotFileParser

import logging
logger = logging.getLogger(__name__)

def check_robots_txt(url: str, useragent="*") -> bool:
    """Check whether url is allowed by robots.txt"""
    rp = RobotFileParser()
    robots_url = f"{url.rstrip('/')}/robots.txt"
    logger.debug("robots.txt check at %s", robots_url)
    rp.set_url(robots_url)

    try:
        rp.read()
        return rp.can_fetch(useragent, url)
    except Exception as e:
        logger.error(f"Parsing robots.txt failed: %s", str(e), exc_info=True)
        return False 

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
            if not check_robots_txt(url):
                logger.warning("Fetching is not allowed by robots.txt (%s)", url)
                return []
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