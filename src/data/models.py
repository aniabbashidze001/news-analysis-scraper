"""
Data model definitions for news article records.

Defines the NewsArticle dataclass used across the scraping and processing pipeline.
"""

from dataclasses import dataclass


@dataclass
class NewsArticle:
    """
        Represents a single news article with core metadata fields.

        Attributes:
            title (str): The title of the article.
            link (str): The URL link to the full article.
            category (str): The category or tag of the article (e.g., politics, tech).
            published (str): The publication timestamp in ISO 8601 format.
            source (str): The source domain or platform (e.g., 'npr.org').
    """
    title: str
    link: str
    category: str
    published: str
    source: str
