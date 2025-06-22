"""
Database module for managing storage of news articles in a SQLite database.

Includes functions to create the articles table, establish database connections,
and insert cleaned article data.
"""

from src.data.models import NewsArticle
from typing import List
import sqlite3
import os

DB_PATH = "data_output/news_articles.db"


def get_connection():
    """
        Establishes and returns a connection to the SQLite database.

        Ensures the 'data_output' directory exists before connecting.

        Returns:
            sqlite3.Connection: SQLite database connection object.
    """
    os.makedirs("data_output", exist_ok=True)
    return sqlite3.connect(DB_PATH)


def create_table():
    """
        Creates the 'articles' table in the SQLite database if it does not exist.

        The table includes columns: id, title, link (unique), category, published, and source.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                link TEXT UNIQUE,
                category TEXT,
                published TEXT,
                source TEXT
            )
        """
        )
        conn.commit()


def insert_articles(articles: List[NewsArticle]):
    """
        Inserts a list of NewsArticle objects into the 'articles' table.

        Args:
            articles (List[NewsArticle]): List of cleaned and validated articles to be inserted.

        Notes:
            - Uses INSERT OR IGNORE to avoid duplicate entries based on the 'link' field.
            - Commits all changes after insertions.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        for article in articles:
            try:
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO articles (title, link, category, published, source)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (
                        article.title,
                        article.link,
                        article.category,
                        article.published,
                        article.source,
                    ),
                )
            except Exception as e:
                print(f"Error inserting article: {article.title} -> {e}")
        conn.commit()
