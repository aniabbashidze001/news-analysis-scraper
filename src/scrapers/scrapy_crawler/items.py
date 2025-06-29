"""
Defines the data structure for scraped news articles used by Scrapy.

Each NewsArticle item represents a single article with fields
such as title, link, category, and published date.
"""

import scrapy


class NewsArticle(scrapy.Item):
    """
        Scrapy item representing a news article.

        Attributes:
            title (scrapy.Field): The title of the article.
            link (scrapy.Field): The URL to the full article.
            category (scrapy.Field): The category or topic of the article.
            published (scrapy.Field): The publication date of the article.
    """
    title = scrapy.Field()
    link = scrapy.Field()
    category = scrapy.Field()
    published = scrapy.Field()
