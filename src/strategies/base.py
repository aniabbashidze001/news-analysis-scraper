"""
Defines the abstract base class for all scraper strategy implementations.

This module enables the use of the Strategy design pattern to switch between different
scraping approaches (e.g., static, dynamic, Scrapy) via a unified interface.
"""

from abc import ABC, abstractmethod


class ScraperStrategy(ABC):
    """Abstract base class that defines a standard interface for scraper strategies."""
    @abstractmethod
    def run(self):
        """Execute the scraper logic. Must be implemented by all concrete strategy subclasses."""
        pass
