"""
Factory module for returning appropriate scraper strategy instance
based on the specified scraper type.

Implements the Strategy design pattern for modular and scalable scraping logic.
"""

from src.strategies.base import ScraperStrategy
from src.strategies.static_strategy import StaticScraperStrategy
from src.strategies.dynamic_strategy import DynamicScraperStrategy
from src.strategies.scrapy_strategy import ScrapyScraperStrategy


def get_scraper(scraper_type: str) -> ScraperStrategy:
    """
        Return the corresponding scraper strategy instance based on the type.

        Args:
            scraper_type (str): The type of scraper to use ("static", "dynamic", or "scrapy").

        Returns:
            ScraperStrategy: An instance of the appropriate scraper strategy.

        Raises:
            ValueError: If the scraper_type is unrecognized.
    """
    if scraper_type == "static":
        return StaticScraperStrategy()
    elif scraper_type == "dynamic":
        return DynamicScraperStrategy()
    elif scraper_type == "scrapy":
        return ScrapyScraperStrategy()
    else:
        raise ValueError(f"Unknown scraper type: {scraper_type}")
