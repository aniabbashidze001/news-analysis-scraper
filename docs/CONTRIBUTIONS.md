# Team Contributions

This document outlines the individual contributions of each team member to the News Analysis Scraper project. Tasks have been divided to ensure a fair and even workload across all required deliverables in accordance with the grading rubric.

---

## 👩 Ana Abashidze

**Areas of Responsibility**:
- Dynamic Scraping
  - Implemented Selenium-based dynamic scraper for Euronews
  - Handled CAPTCHA detection and screenshot saving
  - Implemented retry and throttling mechanisms
- CLI Interface & Strategy Pattern
  - Developed CLI tool with argparse for strategy execution
  - Implemented Strategy pattern for scraper selection
- Report Generation
  - HTML report generator with Jinja2 templating
  - Visualizations using `matplotlib` (trend lines, category distribution)
- Logging & Config Management
  - Built logger module with console/file support and YAML-based config
- Documentation
  - Wrote Technical Architecture (`docs/architecture.md`)
  - Wrote User Guide (`docs/user_guide.md`)
- GitHub Setup
  - Initial repo setup

---

## 👩 Elene Topuridze

**Areas of Responsibility**:
- Static Scraping
  - Created static scraper for NPR using BeautifulSoup4
  - Implemented article collection, pagination, and request throttling
- Data Processing & Validation
  - Developed processors for raw data cleanup and deduplication
  - Built article normalization and validation functions
- Trend Analysis & Export
  - Used pandas/numpy to perform statistical analysis
  - Exported results to CSV, Excel, and JSON
- Testing Suite
  - Developed `tests/unit/test_processors.py` with pytest
  - Created integration test for CLI execution
- Documentation
  - Wrote API Reference (`docs/api_reference.md`)

---

## 👨 Danieli Iliaevi

**Areas of Responsibility**:
- Scrapy Crawler
  - Created Scrapy spider for The Verge news archive
  - Handled pagination, item pipeline, and export to raw directory
- Database Integration
  - Designed and created SQLite schema
  - Implemented insertion of cleaned articles into DB
- Protection Mechanisms
  - Implemented user-agent rotation, retry logic, and error handling
- Code Quality & Testing
  - Integrated linting, docstrings, and ensured modular code structure
  - Verified security practices (timeouts, retries, headers)
- Documentation
  - Wrote `CONTRIBUTIONS.md`

---

## 🤝 Collaborative Tasks

- All members participated in:
  - Final review and testing of the application
  - Manual testing and debugging
  - Video demo preparation and voiceover
  - GitHub issue tracking and milestone tagging

---

This distribution ensures that each member contributed to core scraping, architecture, analysis, interface, and documentation components.