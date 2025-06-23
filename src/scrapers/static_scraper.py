"""
Static scraper for NPR News articles using BeautifulSoup and multithreaded requests.

This module fetches articles from NPR's News section and handles:
- Parsing article metadata (title, link, publication date)
- Simulating throttled requests
- Multithreaded scraping for performance
- Handling pagination via 'Load More' requests
- Saving results to JSON format
"""

from bs4 import BeautifulSoup
import json
import os
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.utils.logger import setup_logger
from src.utils.helpers import get_random_user_agent, safe_request, load_config

logger = setup_logger()


def throttle_requests(min_delay, max_delay):
    """Pause execution for a random duration between `min_delay` and `max_delay` to avoid rate limiting."""
    delay = random.uniform(min_delay, max_delay)
    logger.debug(f"⏳ Throttling for {delay:.2f} seconds")
    time.sleep(delay)


def parse_article(article, min_delay, max_delay):
    """Parse a single <article> element from NPR and extract metadata (title, link, date)."""
    try:
        throttle_requests(min_delay, max_delay)
        title_tag = article.select_one("h2.title a")
        title = title_tag.text.strip()
        link = title_tag["href"]
        date_tag = article.select_one("time")
        published = date_tag["datetime"] if date_tag else "N/A"

        logger.debug(f"📰 Parsed article: {title[:50]}...")

        return {
            "title": title,
            "link": link,
            "category": "news",
            "published": published,
        }
    except Exception as e:
        logger.warning(f"⚠️ Skipping article due to error: {e}")
        return None


def run_static_scrapers():
    """Scrape up to 1000 articles from NPR News using static HTML parsing and save them as JSON."""
    logger.info("📡 Starting static scraping for NPR News...")

    config = load_config()
    min_delay = config.get("scraper_settings", {}).get("throttle_min", 1)
    max_delay = config.get("scraper_settings", {}).get("throttle_max", 3)

    base_url = "https://www.npr.org/sections/news/"
    next_url_template = (
        "https://www.npr.org/get/1001/render/partial/next?start={start}&count=24"
    )

    headers = {
        "User-Agent": get_random_user_agent(),
        "Referer": base_url,
        "X-Requested-With": "XMLHttpRequest",
    }
    logger.debug(f"Using User-Agent: {headers['User-Agent']}")

    scraped_data = []

    # Scrape initial page
    response = safe_request(base_url, headers=headers)
    if not response:
        logger.error(f"❌ Failed to fetch initial page: {base_url}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.select("article")
    logger.debug(f"🔎 Found {len(articles)} articles on the initial page")

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(parse_article, article, min_delay, max_delay)
            for article in articles
        ]
        for future in as_completed(futures):
            result = future.result()
            if result:
                scraped_data.append(result)
                if len(scraped_data) >= 1000:
                    logger.info("✅ Reached 1000 articles. Stopping.")
                    break

    # Scrape "Load More" articles
    start = 24
    while len(scraped_data) < 1000:
        page_url = next_url_template.format(start=start)
        logger.debug(f"🔁 Requesting: {page_url}")
        response = safe_request(page_url, headers=headers)
        if not response:
            logger.warning(f"⚠️ Skipping start={start} due to fetch failure.")
            start += 24
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.select("article")
        logger.debug(f"🔎 Found {len(articles)} articles at start={start}")

        if not articles:
            logger.info("📭 No more articles found — ending early.")
            break

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(parse_article, article, min_delay, max_delay)
                for article in articles
            ]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    scraped_data.append(result)
                    if len(scraped_data) >= 1000:
                        logger.info("✅ Reached 1000 articles. Stopping.")
                        break

        start += 24

    os.makedirs("data_output/raw", exist_ok=True)
    output_path = "data_output/raw/npr_static.json"
    with open(output_path, "w") as f:
        json.dump(scraped_data, f, indent=2)

    logger.debug(f"📁 Saved {len(scraped_data)} articles to {output_path}")
    logger.info(f"✅ Scraped and saved {len(scraped_data)} NPR articles.")
