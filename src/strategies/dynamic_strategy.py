"""
Implements the dynamic scraping strategy using Selenium.

This strategy is part of the Strategy design pattern and delegates scraping logic
to the `run_dynamic_scrapers` function defined in the Selenium scraper module.
"""

from src.strategies.base import ScraperStrategy
from src.scrapers.selenium_scraper import run_dynamic_scrapers


class DynamicScraperStrategy(ScraperStrategy):
    """Concrete strategy class for running dynamic (Selenium-based) scrapers."""
    def run(self):
        """Execute the dynamic scraper using Selenium and multithreaded logic."""
        run_dynamic_scrapers()
