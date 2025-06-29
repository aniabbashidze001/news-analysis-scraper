# API Reference

This document provides an overview of the key modules and functions used in the `news-analysis-scraper` project.

---

## Modules Overview

### `src.scrapers.static_scraper`

- **Function:** `run_static_scrapers()`
  - Static scraper for NPR News using requests and BeautifulSoup.
- **Function:** `parse_article(article, min_delay, max_delay)`
  - Parses individual HTML article blocks.
- **Function:** `throttle_requests(min_delay, max_delay)`
  - Adds delay between requests.

---

### `src.scrapers.selenium_scraper`

- **Function:** `run_dynamic_scrapers()`
  - Uses Selenium to scrape Euronews articles with throttling and CAPTCHA detection.

---

### `src.scrapers.scrapy_crawler.scrapy_crwaler`

- **Class:** `GenericNewsSpider`
  - Scrapy spider for extracting article data from The Verge.

---

### `src.data.models`

- **Class:** `NewsArticle`
  - Data model with fields: `title`, `link`, `category`, `published`, `source`.

---

### `src.data.database`

- **Function:** `create_connection()`
  - Connects to SQLite database.
- **Function:** `create_table()`
  - Creates the `articles` table if not exists.
- **Function:** `insert_articles(articles)`
  - Inserts list of articles into the database.

---

### `src.data.processors`

- **Function:** `process_raw_articles()`
  - Reads, validates, deduplicates, and cleans article data from raw files.
- **Function:** `normalize_date(date_str)`
  - Normalizes and parses date strings.
- **Function:** `is_valid_article(article)`
  - Checks if an article has valid data.

---

### `src.analysis.trends`

- **Function:** `generate_stats()`
  - Computes statistics like top categories and trends.
- **Function:** `analyze_keywords(articles)`
  - Extracts top keywords from titles.
- **Function:** `plot_category_distribution(articles)`
  - Saves a bar chart of article counts by category.
- **Function:** `plot_publishing_trend(articles)`
  - Saves a line plot of publishing frequency over time.

---

### `src.analysis.export`

- **Function:** `export_to_csv(articles)`
- **Function:** `export_to_json(articles)`
- **Function:** `export_to_excel(articles)`
  - Save data in multiple formats in `data_output/exports`.

---

### `src.analysis.report_generator`

- **Function:** `generate_html_report(articles)`
  - Generates `summary_report.html` with insights and charts using Jinja2.

---

### `src.cli.interface`

- **Function:** `run_cli()`
  - CLI interface handling commands like `--static`, `--dynamic`, `--scrapy`, `--process`, etc.
- **Function:** `run_interactive_cli()`
  - Interactive CLI mode with input prompts.

---

### `src.utils.helpers`

- **Function:** `get_random_user_agent()`
- **Function:** `safe_request(url, headers, retries, timeout)`
- **Function:** `load_config(path)`
  - Utility functions for HTTP requests and configuration loading.

---

### `src.utils.logger`

- **Function:** `setup_logger(name)`
  - Configures project-wide logging to file and console.

---

### `src.strategies.*`

- Implements Strategy design pattern to abstract scraper types.
- **Classes:** `StaticScraperStrategy`, `DynamicScraperStrategy`, `ScrapyScraperStrategy` (all inherit from `ScraperStrategy`)

---

## Notes

- All modules include detailed logging and error handling.
- Scrapers are modular and interchangeable.
- Data is validated before insertion into the database or analysis pipelines.