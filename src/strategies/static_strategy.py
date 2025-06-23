"""
Implements the static scraping strategy using HTTP requests and HTML parsing.

This strategy integrates the static scraper into the strategy pattern, allowing it
to be executed uniformly alongside other scraper types.
"""

from src.strategies.base import ScraperStrategy
from src.scrapers.static_scraper import run_static_scrapers


class StaticScraperStrategy(ScraperStrategy):
    """Concrete strategy for running static scraping logic using BeautifulSoup and requests."""
    def run(self):
        """Execute the static scraper defined in the static_scraper module."""
        run_static_scrapers()
