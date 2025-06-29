"""
Implements the Scrapy-based scraping strategy.

This strategy runs the Scrapy crawler via a shell command,
integrating it into the unified scraping framework using the Strategy design pattern.
"""

from src.strategies.base import ScraperStrategy
import os


class ScrapyScraperStrategy(ScraperStrategy):
    """Concrete strategy class for running Scrapy-based scrapers."""
    def run(self):
        """Execute the Scrapy spider by invoking a system shell command."""
        os.system("scrapy crawl generic_news_spider")
