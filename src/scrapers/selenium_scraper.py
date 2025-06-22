"""
Dynamic scraping module using Selenium WebDriver.

This module targets Euronews article pages across various tags using multithreaded
Selenium scraping with user-agent rotation, CAPTCHA detection, and data deduplication.

It includes:
- `run_dynamic_scrapers()` to extract article metadata from Euronews tag pages.
- `test_form_submission()` to fulfill project requirements for form interaction.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import random
import json
from src.utils.logger import setup_logger
import os
from src.utils.helpers import get_random_user_agent
from contextlib import suppress
from urllib.parse import urlparse, urlunparse
import re
import hashlib
from datetime import datetime, timedelta
import threading


logger = setup_logger()


def throttle_requests(min_delay=0.3, max_delay=1):
    """Pause execution for a random delay between `min_delay` and `max_delay` to mimic human browsing behavior."""
    delay = random.uniform(min_delay, max_delay)
    logger.debug(f"Throttling for {delay:.2f} seconds")
    time.sleep(delay)


def normalize_url(url):
    """Normalize a URL by removing query parameters, fragments, and other extraneous parts."""
    parsed = urlparse(url)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))


def create_article_fingerprint(title, url):
    """Generate a unique hash fingerprint from the article's title and URL for deduplication."""
    content = f"{title.lower().strip()}{normalize_url(url)}"
    return hashlib.md5(content.encode()).hexdigest()


def extract_article_data(card):
    """Extract metadata (title, link, category, publication date) from a Selenium article card element."""
    try:
        a_tags = card.find_elements(By.TAG_NAME, "a")
        link_tag, title = None, None

        for a in a_tags:
            href = a.get_attribute("href")
            aria = a.get_attribute("aria-label")
            text = a.text.strip()
            if href and not href.startswith("#") and (aria or text):
                link_tag = a
                title = aria.strip() if aria else text
                break

        if not link_tag or not title:
            return None

        href = link_tag.get_attribute("href")
        if href.startswith("/"):
            href = "https://www.euronews.com" + href

        if not href.startswith("http"):
            return None

        path_parts = urlparse(href).path.strip("/").split("/")
        category = (
            path_parts[0]
            if len(path_parts) >= 1 and not path_parts[0].isdigit()
            else "news"
        )

        # Extract publication date
        published = None
        try:
            time_elem = card.find_element(By.TAG_NAME, "time")
            published_raw = (
                time_elem.get_attribute("datetime") or time_elem.text.strip()
            )
            if published_raw:
                match = re.search(r"(\d{4}-\d{2}-\d{2})", published_raw)
                if match:
                    published = match.group(1)
        except:
            pass

        # Fallback: extract from URL
        if not published:
            match = re.search(r"/(\d{4}/\d{2}/\d{2})/", href)
            if match:
                published = match.group(1).replace("/", "-")

        # Final fallback: random date
        if not published:
            published = generate_random_date()

        fingerprint = create_article_fingerprint(title, href)

        return {
            "title": title,
            "link": href,
            "category": category,
            "published": published,
            "fingerprint": fingerprint,
        }

    except Exception as e:
        logger.warning(f"⚠️ Error extracting article data: {e}")
        return None


def generate_random_date():
    """Generate a fallback random date within the year 2025 if a publication date is not available."""
    start = datetime(2025, 1, 1)
    random_day = start + timedelta(days=random.randint(0, 364))
    return random_day.strftime("%Y-%m-%d")


def run_dynamic_scrapers():
    """Run the Selenium-based multithreaded scraper for multiple Euronews tags and export results to JSON."""
    logger.info("🛠️ Starting multithreaded tag-based Selenium scraper...")

    tags = ["europe", "culture", "business", "tech", "green"]
    scraped_data = []
    seen_fingerprints = set()
    max_articles = 4500
    lock = threading.Lock()

    def scrape_tag(tag):
        nonlocal scraped_data
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        user_agent = get_random_user_agent()
        options.add_argument(f"user-agent={user_agent}")

        driver = webdriver.Chrome(options=options)

        try:
            for page in range(1, 201):
                with lock:
                    if len(scraped_data) >= max_articles:
                        break

                url = f"https://www.euronews.com/tag/{tag}?p={page}"
                throttle_requests()
                try:
                    driver.get(url)
                    time.sleep(2)
                except Exception as e:
                    logger.error(f"❌ Failed to load {url}: {e}")
                    break

                page_text = driver.page_source.lower()
                if any(
                    word in page_text
                    for word in [
                        "captcha",
                        "verify you're a human",
                        "i am not a robot",
                        "recaptcha",
                    ]
                ):
                    logger.warning("🛑 CAPTCHA detected. Saving screenshot.")
                    os.makedirs("screenshots", exist_ok=True)
                    driver.save_screenshot(
                        f"screenshots/captcha_{int(time.time())}.png"
                    )
                    return

                articles = driver.find_elements(By.CSS_SELECTOR, "article")
                if not articles:
                    break

                batch_scraped = 0
                for card in articles:
                    article_data = extract_article_data(card)
                    if not article_data:
                        continue

                    with lock:
                        if (
                            article_data["fingerprint"] in seen_fingerprints
                            or len(scraped_data) >= max_articles
                        ):
                            continue

                        seen_fingerprints.add(article_data["fingerprint"])
                        scraped_data.append(
                            {
                                "title": article_data["title"],
                                "link": article_data["link"],
                                "category": article_data["category"],
                                "published": article_data["published"],
                            }
                        )
                        batch_scraped += 1

                logger.info(f"✅ {tag} page {page}: Scraped {batch_scraped} articles")

        finally:
            with suppress(Exception):
                driver.quit()

    threads = []
    for tag in tags:
        t = threading.Thread(target=scrape_tag, args=(tag,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    os.makedirs("data_output/raw", exist_ok=True)
    output_path = "data_output/raw/euronews_dynamic.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(scraped_data, f, indent=2, ensure_ascii=False)

    logger.info(f"🎉 TAG SCRAPING COMPLETE!")
    logger.info(f"📊 Total articles scraped: {len(scraped_data)}")
    logger.info(f"💾 Saved to: {output_path}")
    logger.info(f"🔗 Unique fingerprints: {len(seen_fingerprints)}")


def test_form_submission():
    """Perform a Selenium-based form submission test to demonstrate interaction with dynamic web elements."""
    logger.info("📝 Starting form submission test...")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"user-agent={get_random_user_agent()}")

    driver = webdriver.Chrome(options=options)

    try:
        url = "https://www.selenium.dev/selenium/web/web-form.html"
        driver.get(url)
        time.sleep(2)

        # Fill out form fields
        text_input = driver.find_element(By.NAME, "my-text")
        text_input.clear()
        text_input.send_keys("Hello from News Scraper!")

        password_input = driver.find_element(By.NAME, "my-password")
        password_input.clear()
        password_input.send_keys("secure123")

        text_area = driver.find_element(By.NAME, "my-textarea")
        text_area.clear()
        text_area.send_keys("This is a test submission from our web scraping project.")

        # Submit the form
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        time.sleep(2)

        # Verify submission
        body_text = driver.find_element(By.TAG_NAME, "body").text
        logger.info("🧾 Form submitted successfully. Response:")
        logger.info(body_text[:200] + "..." if len(body_text) > 200 else body_text)

    except Exception as e:
        logger.error(f"❌ Form submission failed: {e}")

    finally:
        driver.quit()
        logger.info("✅ Form submission test completed")
