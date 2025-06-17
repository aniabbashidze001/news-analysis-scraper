from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import json
from src.utils.logger import setup_logger
import os

logger = setup_logger()

def run_dynamic_scrapers():
    logger.info("Starting dynamic scraping on Euronews...")

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    url = "https://www.euronews.com/news"
    driver.get(url)
    time.sleep(3)

    articles = driver.find_elements(By.CSS_SELECTOR, "div.o-block-listing__item")

    scraped_data = []

    for article in articles[:20]:  # First 20 articles
        try:
            title = article.find_element(By.CSS_SELECTOR, "a.m-object__title").text.strip()
            link = article.find_element(By.CSS_SELECTOR, "a.m-object__title").get_attribute("href")
            category = article.find_element(By.CSS_SELECTOR, ".m-object__section").text.strip()
            date = article.find_element(By.CSS_SELECTOR, ".m-object__date").text.strip()

            scraped_data.append({
                "title": title,
                "link": link,
                "category": category,
                "published": date
            })
        except Exception as e:
            logger.warning(f"Skipping article due to error: {e}")

    driver.quit()

    os.makedirs("data_output/raw", exist_ok=True)
    with open("data_output/raw/euronews_dynamic.json", "w") as f:
        json.dump(scraped_data, f, indent=2)

    logger.info(f"Scraped {len(scraped_data)} articles from Euronews.")
