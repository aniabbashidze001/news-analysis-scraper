"""
Processing pipeline for raw scraped news articles.

This module handles validation, deduplication, date normalization,
and conversion of raw data into structured format for storage and analysis.
"""

from src.data.models import NewsArticle
from src.data.database import insert_articles
import os
import json
import re
from datetime import datetime
from src.utils.logger import setup_logger

logger = setup_logger()

RAW_DIR = "data_output/raw"
PROCESSED_PATH = "data_output/processed/cleaned_articles.json"


def normalize_date(date_str):
    """
    Normalize various date string formats into standardized YYYY-MM-DD format.

    Args:
        date_str (str): Raw date string from article metadata.

    Returns:
        str or None: Normalized date in YYYY-MM-DD format, or None if parsing fails.
    """
    if not date_str or not isinstance(date_str, str):
        return None
    try:
        # Handle common formats: ISO, yyyy-mm-dd, yyyy/mm/dd, etc.
        date_match = re.search(r"\d{4}[-/]\d{2}[-/]\d{2}", date_str)
        if date_match:
            dt = datetime.strptime(
                date_match.group(),
                "%Y-%m-%d" if "-" in date_match.group() else "%Y/%m/%d",
            )
            return dt.strftime("%Y-%m-%d")
    except Exception:
        pass
    return None


def is_valid_article(article):
    """
    Validate if an article has all required fields with appropriate formats.

    Args:
        article (dict): Raw article dictionary.

    Returns:
        bool: True if article is valid, False otherwise.
    """
    return (
        isinstance(article.get("title"), str)
        and article["title"].strip()
        and isinstance(article.get("link"), str)
        and article["link"].startswith("http")
        and normalize_date(article.get("published")) is not None
    )


def process_raw_articles():
    """
        Process all JSON files in the raw data directory.

        - Deduplicates articles by link.
        - Validates essential fields.
        - Normalizes publication dates.
        - Saves cleaned articles to a JSON file.

        Returns:
            list[dict]: A list of cleaned and valid articles.
    """
    logger.info("🧹 Starting raw article processing...")
    seen_links = set()
    cleaned_articles = []
    skipped_files = 0
    skipped_articles = 0

    for filename in os.listdir(RAW_DIR):
        if filename.endswith(".json"):
            path = os.path.join(RAW_DIR, filename)
            logger.debug(f"📄 Reading file: {filename}")
            with open(path, "r", encoding="utf-8") as f:
                try:
                    articles = json.load(f)
                except json.JSONDecodeError:
                    logger.warning(f"⚠️ Skipping {filename}: invalid JSON.")
                    skipped_files += 1
                    continue

                logger.debug(f"🔍 {len(articles)} articles found in {filename}")
                for article in articles:
                    link = article.get("link")
                    if not link or link in seen_links:
                        skipped_articles += 1
                        continue

                    if is_valid_article(article):
                        article["published"] = normalize_date(article["published"])
                        seen_links.add(link)
                        cleaned_articles.append(article)
                    else:
                        logger.debug(
                            f"🚫 Skipping invalid article: {article.get('title', 'N/A')}"
                        )
                        skipped_articles += 1

    os.makedirs(os.path.dirname(PROCESSED_PATH), exist_ok=True)
    with open(PROCESSED_PATH, "w", encoding="utf-8") as f:
        json.dump(cleaned_articles, f, indent=2, ensure_ascii=False)

    logger.info(
        f"✅ Cleaned {len(cleaned_articles)} unique valid articles saved to {PROCESSED_PATH}"
    )
    logger.info(
        f"⚠️ Skipped {skipped_articles} articles due to invalid or duplicate data"
    )
    if skipped_files > 0:
        logger.info(f"⚠️ Skipped {skipped_files} files due to invalid JSON.")
    return cleaned_articles


def process_and_save_all_articles():
    """
        Full processing pipeline to:
        - Clean and validate raw scraped data.
        - Convert it to NewsArticle objects.
        - Insert into the SQLite database.
    """
    logger.info("💾 Starting full article processing and database insertion...")
    raw_articles = process_raw_articles()

    article_objs = [
        NewsArticle(
            title=a.get("title", "N/A"),
            link=a.get("link", "N/A"),
            category=a.get("category", "N/A"),
            published=a.get("published", "N/A"),
            source="merged",
        )
        for a in raw_articles
    ]

    insert_articles(article_objs)
    logger.info(f"🗃️ Inserted {len(article_objs)} articles into the database.")
