# User Guide: News Analysis Scraper

Welcome to the **News Analysis Scraper** user guide! This document provides comprehensive instructions for setting up, installing, and using the scraping system, along with CLI usage examples.

---

## 📦 Overview

This system collects and processes news articles from multiple sources, cleans and stores them in a database, and generates visual reports for trend analysis.

Sources include:
- **Euronews** (Dynamic/Selenium-based)
- **The Verge** (Scrapy-based)
- **NPR News** (Static scraping with BeautifulSoup)

---

## ⚙️ Requirements

Ensure you have the following installed:

- Python 3.9+
- pip (Python package manager)
- Google Chrome (for Selenium)
- ChromeDriver (match your Chrome version)
- [Optional] Virtualenv for isolated environments

---

## 📁 Installation Instructions

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/aniabbashidze001/news-analysis-scraper.git
   cd news-analysis-scraper
   ```

2. **Create and Activate Virtual Environment (optional but recommended)**  
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Configuration**  
   Review the `config/settings.yaml` file and adjust logging or scraping settings if necessary.

---

## 🚀 Running the Application

The tool provides a Command-Line Interface (CLI) to control functionality.

### Syntax:
```bash
python main.py [options]
```

### Available Options:
- `--run-static` – Scrape articles using static scraper (NPR)
- `--run-dynamic` – Scrape using dynamic Selenium-based scraper (Euronews)
- `--run-scrapy` – Scrape using Scrapy (The Verge)
- `--process` – Clean and deduplicate raw data
- `--analyze` – Perform trend analysis and store summaries
- `--report` – Generate HTML visual reports
- `--export` – Export processed data (CSV, JSON, XLSX)
- `--help` – Show CLI usage help

### Example Usage:
```bash
python main.py --run-static
python main.py --process
python main.py --analyze
python main.py --report
```

---

## 📊 Output Files

- Raw data: `data_output/raw/*.json`
- Cleaned data: `data_output/processed/cleaned_articles.json`
- Database: `data_output/news_articles.db`
- Reports: `data_output/reports/summary_report.html`
- Exports: `data_output/exports/articles.csv`, `.json`, `.xlsx`
- Logs: `logs/project.log`

---

## 🧪 Testing

Run unit and integration tests using `pytest`:

```bash
# Unit tests
PYTHONPATH=$(pwd) pytest tests/unit/

# Integration test (process flow)
PYTHONPATH=$(pwd) pytest tests/integration/
```

---

## 🛠️ Troubleshooting

- **ChromeDriver errors**: Ensure ChromeDriver version matches your installed Chrome browser.
- **No output or empty file**: Check the source website and throttling configuration.
- **Scrapy not running**: Ensure Scrapy is installed, and run from the root directory.

---

## 🙋 Need Help?

For issues or questions, please open a GitHub issue or contact the development team.

---

Enjoy exploring trends in online news! 📰📈