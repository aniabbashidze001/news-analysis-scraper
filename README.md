# 📰 News Analysis Scraper

A modular, multi-source news scraping and analysis system that aggregates articles from major online news platforms, cleans and processes the data, performs trend analysis, and generates insightful reports—all through a powerful command-line interface (CLI).

## 🚀 Project Overview

This project was developed as the final deliverable for the Python Data Scraping course. It is capable of:
- Scraping **over 5000 articles** from multiple sources
- Handling **static**, **dynamic**, and **Scrapy-based** scraping strategies
- Performing data cleaning, validation, and trend analysis
- Exporting data and generating visual HTML reports
- Providing a user-friendly CLI interface
- Supporting scheduled automation and logging

## 🔍 Features

- ✅ Multi-source scraping:
  - NPR (Static - BeautifulSoup)
  - Euronews (Dynamic - Selenium)
  - The Verge (Scrapy Framework)
- ✅ Support for anti-bot mechanisms:
  - Randomized user-agent headers
  - CAPTCHA detection with screenshot logging
  - Request throttling
- ✅ Configurable and Modular:
  - Easily extendable with new scraping strategies
  - Configurable via `config/settings.yaml`
- ✅ Trend Analysis & Visualization:
  - Article frequency, keyword heatmaps, publishing patterns
- ✅ Database Integration:
  - Uses SQLite to store cleaned and validated articles
- ✅ Clean, documented codebase:
  - Follows design patterns (Factory, Strategy)
  - Includes full docstrings and test suite

## 🛠️ Setup & Installation

### Requirements
Install dependencies:

```bash
pip install -r requirements.txt
```

### Configuration

Edit your settings in `config/settings.yaml`.

### Run CLI

```bash
# Interactive menu
python main.py

# Run specific operation
python main.py --export
python main.py --process
python main.py --analyze
python main.py --report
```

## 📁 Project Structure

```
news-analysis-scraper/
├── main.py
├── config/
├── data_output/
├── src/
│   ├── scrapers/
│   ├── data/
│   ├── analysis/
│   ├── cli/
│   ├── strategies/
│   ├── factories/
│   ├── utils/
│   └── templates/
├── tests/
├── docs/
```

## 📊 Results

- **5000+** cleaned articles stored in `news_articles.db`
- Trend charts and summary reports in `data_output/reports/`
- Exports available in CSV, JSON, XLSX

## 🧪 Testing

```bash
# Unit tests
PYTHONPATH=$(pwd) pytest tests/unit/

# Integration tests
PYTHONPATH=$(pwd) pytest tests/integration/
```

## 👥 Team Contributions

- **Ana Abashidze** – CLI design, dynamic scraper, HTML report generation, documentation
- **Elene Topuridze** – Static scraper, data cleaning & analysis, API docs
- **Danieli Iliaevi** – Scrapy crawler, database, testing suite

See full breakdown in [`CONTRIBUTIONS.md`](CONTRIBUTIONS.md)

## 📄 Documentation

All documentation is located in `/docs`:
- [Architecture](docs/architecture.md)
- [User Guide](docs/user_guide.md)
- [API Reference](docs/api_reference.md)


## 🏁 GitHub Best Practices

- Descriptive commit messages and release tags
- All team members contributed to Git history
- Project follows modular and testable design

---

Made with 💻 and ☕ by Team News Analysis 🔍