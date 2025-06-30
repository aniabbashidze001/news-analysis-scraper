# System Architecture: News Analysis & Aggregation Scraper

## Overview

The **News Analysis & Aggregation Scraper** is a modular, scalable data scraping and analytics system developed in Python. Its primary purpose is to collect, clean, analyze, and report on news articles from diverse sources using a combination of static HTML scraping, dynamic (JavaScript-rendered) scraping, and Scrapy-based crawling. The project emphasizes flexibility, maintainability, and testability, built with production-grade software engineering practices.

The application consists of multiple interconnected components organized by responsibility and design pattern. These include scraping strategies (Strategy Pattern), a factory-based orchestrator, CLI interfaces, database integration, analysis/reporting modules, and unit/integration tests.

---

## 1. Project Structure

```
news-analysis-scraper/
│
├── main.py                           # CLI entry point
├── config/settings.yaml             # Configurable parameters
├── data_output/                     # Raw, processed, and exported data
├── logs/                            # Runtime logs
├── src/                             # Core application logic
│   ├── scrapers/                    # Static, dynamic, and Scrapy scrapers
│   ├── data/                        # Database schema and processors
│   ├── analysis/                    # Trend analysis and report generation
│   ├── cli/                         # CLI command handling
│   ├── strategies/                  # Strategy pattern for scraper selection
│   ├── factories/                   # Factory class for scraper initialization
│   ├── templates/                   # HTML template for reports
│   └── utils/                       # Logging, config, helpers
├── tests/                           # Unit and integration test suites
└── docs/                            # Markdown-based documentation
```

---

## 2. Core Components

### 2.1 Scrapers

#### a. Static Scraper (`static_scraper.py`)
- Uses `requests` and `BeautifulSoup` to parse NPR articles.
- Employs a thread pool for parallel processing and rate throttling.
- Handles "Load More" logic via AJAX endpoints.

#### b. Dynamic Scraper (`selenium_scraper.py`)
- Built with `Selenium` and `webdriver-manager`.
- Navigates JavaScript-rendered Euronews pages and extracts full article links and titles.
- Implements CAPTCHA detection and logging.

#### c. Scrapy Crawler (`scrapy_crawler.py`)
- Built with `Scrapy`, targeting The Verge’s news archive.
- Implements pagination, item pipelines, and deduplication handling.
- Captures article metadata using Scrapy’s selector engine.

### 2.2 CLI Interface

- Managed through `interface.py`.
- Supports commands like:
  - `--static`, `--dynamic`, `--scrapy` to run specific scrapers.
  - `--process` to clean and validate raw articles.
  - `--analyze` to perform statistical summaries.
  - `--report` to generate HTML and export files.

### 2.3 Data Processing

- `processors.py` loads JSON files from the raw folder, normalizes dates, validates fields, deduplicates entries, and saves them into `cleaned_articles.json`.
- Implements helper functions like `normalize_date()` and `is_valid_article()` with accompanying tests.

### 2.4 Database (`news_articles.db`)

- Managed with `sqlite3` and ORM-style helpers in `models.py`.
- Stores cleaned article data for long-term access and analysis.
- Used in export and report generation.

---

## 3. Design Patterns & Architecture

### Strategy Pattern
Each scraper type (static, dynamic, scrapy) is encapsulated in a separate strategy class implementing the `ScraperStrategy` abstract base. This makes switching or extending scrapers seamless.

### Factory Pattern
`scraper_factory.py` instantiates the correct scraper strategy based on CLI arguments.

### Modularization
Each domain (scraping, data handling, analysis, logging) has its own submodule under `src/`, enabling separation of concerns, unit testing, and team collaboration.

---

## 4. Logging and Error Handling

- Centralized logger via `utils/logger.py`.
- Configurable via `settings.yaml` (log level, log file, enable console).
- Captures retry attempts, page failures, parsing errors, and progress.

---

## 5. Data Flow Pipeline

```
1. CLI Triggers Scraper
    ↓
2. Scraper Collects Raw JSON
    ↓
3. Processor Validates + Cleans Data
    ↓
4. Cleaned Data Saved to DB + JSON
    ↓
5. Analysis Module Performs Aggregation
    ↓
6. Visual Reports + HTML Summary Generated
```

---

## 6. Analysis & Reporting

- `trends.py` calculates publishing trends, top categories, and common keywords.
- `report_generator.py` creates visualizations using `matplotlib` and exports reports in CSV, XLSX, and HTML using Jinja2 templating.
- Summary reports are saved under `data_output/reports`.

---

## 7. Testing Architecture

### Unit Tests
Located in `tests/unit/`, testing core utilities in isolation:
- Article cleaning
- Date normalization
- Validation logic

### Integration Tests
`tests/integration/` includes end-to-end tests like:
- CLI processing command
- Full scraping + processing lifecycle

Test coverage ensures functionality of all core logic paths.

---

## 8. Scalability and Extensibility

- New sources can be added by creating a new strategy class and registering it in the factory.
- Modularized config (user agents, delays) ensures scraper adaptability to changing anti-bot measures.
- Database structure supports longitudinal studies and historical analysis.

---

## 9. Security & Compliance

- Respects robots.txt directives where applicable.
- Implements retry logic and timeouts to avoid hammering servers.
- Follows ethical scraping guidelines (limited concurrency, user-agent rotation).

---

## Conclusion

This system is designed to be resilient, efficient, and flexible for real-world scraping scenarios. It combines industry best practices in software engineering with a practical focus on data analytics. With clean architecture, robust logging, a test suite, and a CLI interface, this application serves as a solid foundation for news data aggregation and analysis at scale.